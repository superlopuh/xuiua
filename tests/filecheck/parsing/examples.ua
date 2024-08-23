# RUN: xuiua lower %s | filecheck %s

Id ← ∘
Dup ← .

# CHECK:       builtin.module {
# CHECK-NEXT:    func.func @Id(%0 : tensor<*xf64>) -> tensor<*xf64> {
# CHECK-NEXT:      func.return %0 : tensor<*xf64>
# CHECK-NEXT:    }
# CHECK-NEXT:    func.func @Dup(%0 : tensor<*xf64>) -> (tensor<*xf64>, tensor<*xf64>) {
# CHECK-NEXT:      func.return %0, %0 : tensor<*xf64>, tensor<*xf64>
# CHECK-NEXT:    }
# CHECK-NEXT:  }
