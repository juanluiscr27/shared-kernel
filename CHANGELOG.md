# Changelog

All notable changes to Shared Kernel will be documented in this file.

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