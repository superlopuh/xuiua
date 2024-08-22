# RUN: xuiua parse %s | filecheck %s --check-prefix=AST
# RUN: xuiua lower %s uiua | filecheck %s --check-prefix=IR-GEN

∘ 5

# AST:       [
# AST-NEXT:    Words(
# AST-NEXT:      [
# AST-NEXT:        [
# AST-NEXT:          121-122: IDENTITY,
# AST-NEXT:          122-123: <spaces>,
# AST-NEXT:          123-124: "5",
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
