# RUN: xuiua parse %s | filecheck %s --check-prefix=AST
# RUN: xuiua lower %s | filecheck %s --check-prefix=IR-GEN
# RUN: xuiua lower %s 'add-shapes{shapes="Add=2x3_2x3"},shape-inference' | filecheck %s

Add ← +

# AST:       [
# AST-NEXT:    Binding(
# AST-NEXT:      name: Add,
# AST-NEXT:      public: True,
# AST-NEXT:      array_macro: False,
# AST-NEXT:      signature: None
# AST-NEXT:      words: [
# AST-NEXT:        {{\d+}}-{{\d+}}: <spaces>,
# AST-NEXT:        {{\d+}}-{{\d+}}: ADD,
# AST-NEXT:      ],
# AST-NEXT:    ),
# AST-NEXT:  ]

# IR-GEN:       builtin.module {
# IR-GEN-NEXT:    func.func @Add(%0 : tensor<*xf64>, %1 : tensor<*xf64>) -> tensor<*xf64> {
# IR-GEN-NEXT:      %2 = "uiua.add"(%0, %1) : (tensor<*xf64>, tensor<*xf64>) -> tensor<*xf64>
# IR-GEN-NEXT:      func.return %2 : tensor<*xf64>
# IR-GEN-NEXT:    }
# IR-GEN-NEXT:  }

# CHECK:       builtin.module {
# CHECK-NEXT:    func.func @Add(%0 : tensor<2x3xf64>, %1 : tensor<2x3xf64>) -> tensor<*xf64> {
# CHECK-NEXT:      %2 = "uiua.add"(%0, %1) : (tensor<2x3xf64>, tensor<2x3xf64>) -> tensor<2x3xf64>
# CHECK-NEXT:      %3 = "uiua.cast"(%2) : (tensor<2x3xf64>) -> tensor<*xf64>
# CHECK-NEXT:      func.return %3 : tensor<*xf64>
# CHECK-NEXT:    }
# CHECK-NEXT:  }
