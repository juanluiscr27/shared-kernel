from sharedkernel.infrastructure.errors import IntegrityError


def test_integrity_error_exception_sets_attributes():
    # Arrange
    class EventStore:
        pass

    source = EventStore()

    # Act
    error = IntegrityError(source=source, entity_id="ACC-001", position=5)

    # Assert
    assert "ACC-001" in str(error)
    assert "position 5" in str(error)
    assert "EventStore" in error.source
