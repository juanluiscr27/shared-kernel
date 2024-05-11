# Changelog

All notable changes to Shared Kernel will be documented in this file.

## 1.0.1 (2024-05-10)

### Add

- qualname and full_qualname property to Entity and DomainEvent base classes.

### Fix

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