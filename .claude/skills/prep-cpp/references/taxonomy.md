# Taxonomy — cpp

## Topic tags
- `value-categories-move`
- `raii-smart-pointers`
- `rule-of-five`
- `object-lifetime-ub`
- `templates-deduction`
- `concepts-constraints`
- `constexpr-consteval`
- `stl-containers-iterators`
- `algorithms-ranges`
- `lambdas-callables`
- `oop-virtual-vtable`
- `exceptions-safety`
- `concurrency-memory-model`
- `coroutines`
- `cpp20-features`

## Flaw codes
Format `F-<AREA>-<WHAT>`. Use the closest existing code; add a new line here if none fits.

| Code | Meaning |
|------|---------|
| `F-CONCEPT-CONFUSION` | Mixed up two related concepts. |
| `F-DEF-WRONG` | Incorrect or imprecise definition. |
| `F-CALC-ERROR` | Arithmetic or formula error in a calculation. |
| `F-TRADEOFF-MISSING` | Gave a mechanism without its cost/benefit trade-off. |
| `F-OVERCONFIDENT` | Wrong at confidence 3. |
| `F-LUCKY-GUESS` | Right at confidence 1 (unreliable knowledge). |
| `F-SCOPE-SHALLOW` | Right headline, missed the key mechanism when asked to go deeper. |
| `F-UB-MISSED` | Did not spot undefined behaviour (dangling, OOB, overflow, data race, aliasing). |
| `F-LIFETIME-ERROR` | Reference/iterator/pointer used after the object died or the container reallocated. |
| `F-MOVE-ERROR` | Misjudged what moves/copies happen, used a moved-from object, or misread value category. |
| `F-OWNERSHIP-ERROR` | Wrong smart-pointer choice or ownership cycle/double ownership. |
| `F-TEMPLATE-DEDUCTION-ERROR` | Wrong deduced type, forwarding reference vs rvalue reference, or overload resolution. |
| `F-SPECIAL-MEMBER-ERROR` | Wrong implicit special members (rule of 0/3/5), slicing, missing virtual destructor. |
| `F-INIT-ORDER` | Initialization/evaluation order assumption (unspecified or member-init order). |
| `F-CONST-CORRECTNESS` | const/mutable/constexpr mistake. |
| `F-STL-MISUSE` | STL pitfall: operator[] inserting, erase-while-iterating, invalid comparator, algorithm precondition violated. |
| `F-CONCURRENCY-ERROR` | Data race, wrong memory_order, lock misuse. |
| `F-STD-VERSION-ERROR` | Attributed a feature to the wrong standard version. |
| `F-COMPILE-PREDICTION` | Mispredicted whether code compiles. |
