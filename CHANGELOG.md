# Changelog

All notable changes to Shared Kernel will be documented in this file.

## 3.4.0 (2024-08-25)

### Added

- ack response model service to parse response from acknowledgement.

## 3.3.0 (2024-08-24)

### Changed

- acknowledgement data entity id data type to UUID.
- error detail reason for context error.

## 3.2.0 (2024-07-19)

### Added

- model type property to projection generic base class.
- detect class to validate text input against sql injection.

### Changed

- aggregate apply method move it inside raise event method.

## 3.1.0 (2024-06-21)

- log level inside register and subscribe method.
- call to get handled types using the projection type.
- type inspection dependency version to 0.5.0.

## 3.0.1 (2024-06-12)

### Fixed

- to event deserializer function extracting quoted JSON string to valid JSON string.

## 3.0.0 (2024-06-09)

### Added

- logging to application and infrastructure services.
- function to map from object to event.

### Changed

- event handlers parameter list to include event position to support idempotency.
- projector process event method implementation.
- mapping pipeline and mapping behavior class structure.
- command ack position property to version.

### Fixed

- projection handled types properties to return only type name.

## 2.3.0 (2024-05-23)

### Added

- correlation id to event data model.
- API Error class.

### Changed

- repository aggregate type to return only the name of the super type.

## 2.2.0 (2024-05-22)

### Added

- Request Mapper and Mapping Behavior.

### Changed

- Rejection status property name to status_code.

## 2.1.1 (2024-05-21)

### Fixed

- ErrorDetail asdict method to return a dictionary.

## 2.1.0 (2024-05-21)

### Added

- json encoder class for UUID values.

## 2.0.0 (2024-05-20)

### Added

- an acknowledgement response data model together with a command status enum.
- a service bus implementation to send commands and queries.
- event mapper base class, mapping behavior and mapping pipeline.

### Fixed

- aggregate_type property access to the generic super type of base repository.

### Changed

- exception class hierarchy and internal properties.
- command handler to be generic handler of commands.
- query handler to a generic handler of queries.
- validators to be generic validator of requests.
- event broker subscribe method to get handler type from generics.
- event data model, adding created field.
- version of type inspection dependency.
- Test implementations.

## 1.0.1 (2024-05-10)

### Added

- qualname and full_qualname property to Entity and DomainEvent base classes.
- application error and infrastructure error.

### Fixed

- setup config version number.

## 1.0.0 (2024-05-08)

### Changed

- Repository abstract class to be generic by entity type.
  It does not implement any method, but it has an aggregate type property.

### Added

- Projectors as event handlers in the infrastructure layer. Includes projections to transform events to data models.
- Event dispatcher to the infrastructure layer to map events to corresponding event handlers (projectors).
- typeinspection as a new dependency

## 0.1.0-beta (2024-04-22)

### Added

- Value Objects, Domain Entities, Aggregates
- Domain Service
- CQRS Pattern with Commands, Queries and Handlers
- Domain Events and Event Handlers
- Guard Clauses
- Command Validator
- Domain Errors
- Event Broker (in memory)
- Event Dispatcher
- Repository Pattern
- Projections
- API Contracts
- Clean Architecture