# RUN: xuiua parse %s | filecheck %s --check-prefix=AST
# RUN: xuiua lower %s | filecheck %s --check-prefix=IR-GEN

×3 5
# ×2 [1 2 3]
# × [1 2 3] [4 5 6]
# × [¯1 0 1] "hey"

# AST:       [
# AST-NEXT:    Words(
# AST-NEXT:      [
# AST-NEXT:        [
# AST-NEXT:          {{\d+}}-{{\d+}}: MULTIPLY,
# AST-NEXT:          {{\d+}}-{{\d+}}: "3",
# AST-NEXT:          {{\d+}}-{{\d+}}: <spaces>,
# AST-NEXT:          {{\d+}}-{{\d+}}: "5",
# AST-NEXT:        ],
# AST-NEXT:      ]
# AST-NEXT:    ),
# AST-NEXT:  ]

# IR-GEN:       builtin.module {
# IR-GEN-NEXT:    func.func @uiua_main() -> tensor<*xf64> {
# IR-GEN-NEXT:      %0 = arith.constant dense<5.000000e+00> : tensor<1xf64>
# IR-GEN-NEXT:      %1 = arith.constant dense<3.000000e+00> : tensor<1xf64>
# IR-GEN-NEXT:      %2 = "uiua.multiply"(%0, %1) : (tensor<1xf64>, tensor<1xf64>) -> tensor<*xf64>
# IR-GEN-NEXT:      func.return %2 : tensor<*xf64>
# IR-GEN-NEXT:    }
# IR-GEN-NEXT:  }
