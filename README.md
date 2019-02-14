# STRIPS-problem-solving
Solve the problem of order delivering using STRIPS.

###### The representation of the plan operators:

**Fly(startCell, stopCell)**
* Preconditions: Position(startCell)
* Postconditions: Position(stopCell)
* Deletions: Position(startCell)

**Load(productId, position)**
* Preconditions: Empty(), Position(position),Warehouse(position), hasProduct (position, productId)
* Postconditions: Carries(productId)
* Deletions: Empty()

**Deliver(productId, position)**
* Preconditions: Carries(productId), Position(position), Client(position), Order(position, productId) 
* Postconditions: Empty(), OrderCompleted(position, productId) 
* Deletions: Carries(productId)

The goals are represented by OrderCompleted predicate.
