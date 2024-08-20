# RUN: xuiua parse %s | filecheck %s --check-prefix=AST

NumOne ← 1
NumTwo ← 2
# 😀 ← "happy"

# AST:       [
# AST-NEXT:    Words(
# AST-NEXT:      [
# AST-NEXT:      ]
# AST-NEXT:    ),
# AST-NEXT:    Binding(
# AST-NEXT:      name: NumOne,
# AST-NEXT:      public: True,
# AST-NEXT:      array_macro: False,
# AST-NEXT:      signature: None
# AST-NEXT:      words: [
# AST-NEXT:        65-66: <spaces>,
# AST-NEXT:        66-67: "1",
# AST-NEXT:      ],
# AST-NEXT:    ),
# AST-NEXT:    Binding(
# AST-NEXT:      name: NumTwo,
# AST-NEXT:      public: True,
# AST-NEXT:      array_macro: False,
# AST-NEXT:      signature: None
# AST-NEXT:      words: [
# AST-NEXT:        76-77: <spaces>,
# AST-NEXT:        77-78: "2",
# AST-NEXT:      ],
# AST-NEXT:    ),
# AST-NEXT:    Words(
# AST-NEXT:      [
# AST-NEXT:      ]
# AST-NEXT:    ),
# AST-NEXT:  ]
