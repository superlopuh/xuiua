# RUN: xuiua parse %s | filecheck %s --check-prefix=AST

NumOne ← 1
NumTwo ← 2
# 😀 ← "happy"

# AST:       [
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
# AST-NEXT:  ]

# IR-GEN:       builtin.module {
# IR-GEN-NEXT:    func.func @NumOne() -> tensor<*xf64> {
# IR-GEN-NEXT:      %0 = arith.constant 1.000000e+00 : f64
# IR-GEN-NEXT:      func.return %0 : f64
# IR-GEN-NEXT:    }
# IR-GEN-NEXT:    func.func @NumTwo() -> tensor<*xf64> {
# IR-GEN-NEXT:      %0 = arith.constant 2.000000e+00 : f64
# IR-GEN-NEXT:      func.return %0 : f64
# IR-GEN-NEXT:    }
# IR-GEN-NEXT:  }
