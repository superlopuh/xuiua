# RUN: xuiua parse %s | filecheck %s --check-prefix=AST
# RUN: xuiua lower %s | filecheck %s --check-prefix=IR-GEN

∘ 5

# AST:       [
# AST-NEXT:    Words(
# AST-NEXT:      [
# AST-NEXT:        [
# AST-NEXT:          116-117: IDENTITY,
# AST-NEXT:          117-118: <spaces>,
# AST-NEXT:          118-119: "5",
# AST-NEXT:        ],
# AST-NEXT:      ]
# AST-NEXT:    ),
# AST-NEXT:  ]

# IR-GEN:       builtin.module {
# IR-GEN-NEXT:    func.func @uiua_main() -> tensor<1xf64> {
# IR-GEN-NEXT:      %0 = arith.constant dense<5.000000e+00> : tensor<1xf64>
# IR-GEN-NEXT:      func.return %0 : tensor<1xf64>
# IR-GEN-NEXT:    }
# IR-GEN-NEXT:  }
