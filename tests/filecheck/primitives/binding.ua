# RUN: xuiua parse %s | filecheck %s --check-prefix=AST
# RUN: xuiua lower %s | filecheck %s --check-prefix=IR-GEN

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
# AST-NEXT:        124-125: <spaces>,
# AST-NEXT:        125-126: "1",
# AST-NEXT:      ],
# AST-NEXT:    ),
# AST-NEXT:    Binding(
# AST-NEXT:      name: NumTwo,
# AST-NEXT:      public: True,
# AST-NEXT:      array_macro: False,
# AST-NEXT:      signature: None
# AST-NEXT:      words: [
# AST-NEXT:        135-136: <spaces>,
# AST-NEXT:        136-137: "2",
# AST-NEXT:      ],
# AST-NEXT:    ),
# AST-NEXT:  ]

# IR-GEN:       builtin.module {
# IR-GEN-NEXT:    func.func @NumOne() -> tensor<1xf64> {
# IR-GEN-NEXT:      %0 = arith.constant dense<1.000000e+00> : tensor<1xf64>
# IR-GEN-NEXT:      func.return %0 : tensor<1xf64>
# IR-GEN-NEXT:    }
# IR-GEN-NEXT:    func.func @NumTwo() -> tensor<1xf64> {
# IR-GEN-NEXT:      %0 = arith.constant dense<2.000000e+00> : tensor<1xf64>
# IR-GEN-NEXT:      func.return %0 : tensor<1xf64>
# IR-GEN-NEXT:    }
# IR-GEN-NEXT:  }
