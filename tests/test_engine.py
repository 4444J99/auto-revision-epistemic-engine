"""
Tests for the Auto-Revision Epistemic Engine
"""

from auto_revision_epistemic_engine import AutoRevisionEngine


class TestAutoRevisionEngine:
    """Test cases for the main engine"""

    def test_engine_initialization(self):
        """Test that engine initializes correctly"""
        engine = AutoRevisionEngine(
            pipeline_id="test_pipeline",
            random_seed=42,
        )
        assert engine.config.pipeline_id == "test_pipeline"
        assert engine.config.random_seed == 42

    def test_pipeline_execution(self, tmp_path):
        """Test basic pipeline execution"""
        engine = AutoRevisionEngine(
            pipeline_id="test_execution",
            random_seed=123,
            audit_log_dir=str(tmp_path / "audit"),
            state_dir=str(tmp_path / "state"),
        )
        
        result = engine.execute(
            inputs={"data": {"records": 10}}
        )
        
        assert result["success"] is True
        assert "outputs" in result
        assert "pipeline_status" in result

    def test_pipeline_status(self, tmp_path):
        """Test pipeline status reporting"""
        engine = AutoRevisionEngine(
            pipeline_id="test_status",
            random_seed=456,
            audit_log_dir=str(tmp_path / "audit"),
            state_dir=str(tmp_path / "state"),
        )
        
        engine.execute(inputs={"data": {"records": 5}})
        status = engine.get_status()
        
        assert status["pipeline_id"] == "test_status"
        assert status["completed"] is True
        assert status["audit_chain_valid"] is True

    def test_model_pinning(self, tmp_path):
        """Test model version pinning"""
        engine = AutoRevisionEngine(
            pipeline_id="test_pin",
            random_seed=789,
            audit_log_dir=str(tmp_path / "audit"),
            state_dir=str(tmp_path / "state"),
        )
        
        engine.pin_model("test-model", "v1.0.0")
        repro = engine.get_reproducibility_info()
        
        assert "test-model" in repro["model_pins"]
        assert repro["model_pins"]["test-model"] == "v1.0.0"

    def test_audit_trail(self, tmp_path):
        """Test audit trail creation"""
        engine = AutoRevisionEngine(
            pipeline_id="test_audit_trail",
            random_seed=101,
            audit_log_dir=str(tmp_path / "audit"),
            state_dir=str(tmp_path / "state"),
        )
        
        engine.execute(inputs={"data": {"records": 3}})
        audit = engine.get_audit_trail()
        
        assert audit["chain_valid"] is True
        assert audit["total_entries"] > 0
        assert len(audit["attestations"]) >= 3  # At least 3 attestations

    def test_ethics_axiom(self, tmp_path):
        """Test adding custom ethical axiom"""
        engine = AutoRevisionEngine(
            pipeline_id="test_ethics",
            random_seed=202,
            audit_log_dir=str(tmp_path / "audit"),
            state_dir=str(tmp_path / "state"),
        )
        
        engine.add_ethical_axiom(
            axiom_id="TEST_001",
            category="TRANSPARENCY",
            statement="Test axiom",
            weight=1.0,
        )
        
        ethics = engine.get_ethics_report()
        assert ethics["enabled"] is True
        assert ethics["axiom_count"] > 8  # Default 8 + custom 1


class TestAuditLogger:
    """Test cases for audit logging"""

    def test_audit_log_creation(self, tmp_path):
        """Test audit log creation"""
        from auto_revision_epistemic_engine.audit import AuditLogger
        
        logger = AuditLogger(log_dir=str(tmp_path / "audit_logger"))
        entry = logger.log_event(
            event_type="TEST_EVENT",
            actor="TEST_ACTOR",
            action="Test action",
        )
        
        assert entry.event_type == "TEST_EVENT"
        assert entry.actor == "TEST_ACTOR"
        assert entry.entry_hash is not None

    def test_audit_chain_integrity(self, tmp_path):
        """Test audit chain integrity verification"""
        from auto_revision_epistemic_engine.audit import AuditLogger
        
        logger = AuditLogger(log_dir=str(tmp_path / "audit_chain"))
        
        for i in range(5):
            logger.log_event(
                event_type=f"EVENT_{i}",
                actor="SYSTEM",
                action=f"Action {i}",
            )
        
        assert logger.verify_chain() is True


class TestStateManager:
    """Test cases for state management"""

    def test_state_snapshot_creation(self, tmp_path):
        """Test state snapshot creation"""
        from auto_revision_epistemic_engine.reproducibility import StateManager
        
        manager = StateManager(state_dir=str(tmp_path / "state_mgr"), random_seed=42)
        
        snapshot = manager.create_snapshot(
            state_id="test_snapshot",
            phase="TEST_PHASE",
            data={"key": "value"},
        )
        
        assert snapshot.state_id == "test_snapshot"
        assert snapshot.phase == "TEST_PHASE"
        assert snapshot.state_hash is not None

    def test_snapshot_verification(self, tmp_path):
        """Test state snapshot verification"""
        from auto_revision_epistemic_engine.reproducibility import StateManager
        
        manager = StateManager(state_dir=str(tmp_path / "state_verify"), random_seed=123)
        
        manager.create_snapshot(
            state_id="verify_test",
            phase="VERIFY_PHASE",
            data={"test": "data"},
        )
        
        assert manager.verify_snapshot("verify_test") is True


class TestPhaseManager:
    """Test cases for phase management"""

    def test_phase_execution(self):
        """Test phase execution tracking"""
        from auto_revision_epistemic_engine.phases import PhaseManager, PhaseName
        
        manager = PhaseManager()
        execution = manager.start_phase(
            PhaseName.INGESTION,
            inputs={"data": "test"},
        )
        
        assert execution.phase == PhaseName.INGESTION
        assert execution.status.value == "RUNNING"
        
        manager.complete_phase(
            execution.execution_id,
            outputs={"result": "completed"},
        )
        
        assert execution.status.value == "COMPLETED"


class TestResourceOptimization:
    """Test cases for resource optimization"""

    def test_resource_allocation(self):
        """Test resource allocation"""
        from auto_revision_epistemic_engine.rol_t import (
            ResourceOptimizationLayer,
            ResourceType,
        )
        
        rol_t = ResourceOptimizationLayer()
        
        allocation = rol_t.allocate_resource(
            resource_type=ResourceType.COMPUTE,
            phase="TEST_PHASE",
            amount_requested=100.0,
            unit="units",
            priority=7,
        )
        
        assert allocation.resource_type == ResourceType.COMPUTE
        assert allocation.amount_requested == 100.0
        assert allocation.amount_allocated > 0

    def test_resource_usage_tracking(self):
        """Test resource usage tracking"""
        from auto_revision_epistemic_engine.rol_t import (
            ResourceOptimizationLayer,
            ResourceType,
        )
        
        rol_t = ResourceOptimizationLayer()
        
        allocation = rol_t.allocate_resource(
            resource_type=ResourceType.MEMORY,
            phase="TEST_PHASE",
            amount_requested=1024.0,
            unit="MB",
            priority=9,  # High priority gets full allocation
        )
        
        usage = rol_t.record_usage(
            allocation_id=allocation.allocation_id,
            amount_used=900.0,
        )
        
        assert usage.amount_used == 900.0
        # With high priority, we get full allocation, so waste should be positive
        assert usage.efficiency <= 1.0
        assert usage.efficiency > 0.0


class TestEthicsFramework:
    """Test cases for ethics framework"""

    def test_normative_audit(self):
        """Test normative audit"""
        from auto_revision_epistemic_engine.ethics import AxiomFramework
        
        framework = AxiomFramework()
        
        audit = framework.conduct_normative_audit(
            phase="TEST_PHASE",
            evaluation_context={
                "actor": "SYSTEM",
                "rationale": "Test audit",
            },
        )
        
        assert audit.phase == "TEST_PHASE"
        assert len(audit.axioms_evaluated) > 0
        assert audit.compliance_score >= 0.0


class TestHumanReviewGate:
    """Test cases for Human Review Gates"""

    def test_review_request(self):
        """Test review request creation"""
        from auto_revision_epistemic_engine.hrg import HumanReviewGate
        
        hrg = HumanReviewGate()
        
        review = hrg.request_review(
            gate_name="TEST_GATE",
            phase="TEST_PHASE",
            assigned_to="test_reviewer",
        )
        
        assert review.gate_name == "TEST_GATE"
        assert review.assigned_to == "test_reviewer"
        assert review.status.value == "PENDING"

    def test_review_completion(self):
        """Test review completion"""
        from auto_revision_epistemic_engine.hrg import HumanReviewGate
        
        hrg = HumanReviewGate()
        
        review = hrg.request_review(
            gate_name="TEST_GATE_2",
            phase="TEST_PHASE_2",
            assigned_to="reviewer",
        )
        
        hrg.start_review(review.review_id, "reviewer")
        hrg.complete_review(
            review.review_id,
            decision="APPROVE",
            rationale="Test approval",
        )
        
        assert review.status.value == "APPROVED"
        assert review.decision == "APPROVE"
