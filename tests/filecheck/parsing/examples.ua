# RUN: xuiua lower %s | filecheck %s

Id ← ∘
Dup ← .
Sum ← /+

# CHECK:       builtin.module {
# CHECK-NEXT:    func.func @Id(%0 : tensor<*xf64>) -> tensor<*xf64> {
# CHECK-NEXT:      func.return %0 : tensor<*xf64>
# CHECK-NEXT:    }
# CHECK-NEXT:    func.func @Dup(%0 : tensor<*xf64>) -> (tensor<*xf64>, tensor<*xf64>) {
# CHECK-NEXT:      func.return %0, %0 : tensor<*xf64>, tensor<*xf64>
# CHECK-NEXT:    }
# CHECK-NEXT:    func.func @Sum(%0 : tensor<*xf64>) -> tensor<*xf64> {
# CHECK-NEXT:      %1 = "uiua.reduce"(%0) ({
# CHECK-NEXT:      ^0(%2 : tensor<*xf64>, %3 : tensor<*xf64>):
# CHECK-NEXT:          %4 = "uiua.add"(%2, %3) : (tensor<*xf64>, tensor<*xf64>) -> tensor<*xf64>
# CHECK-NEXT:          "uiua.yield"(%4) : (tensor<*xf64>) -> ()
# CHECK-NEXT:      }) : (tensor<*xf64>) -> tensor<*xf64>
# CHECK-NEXT:      func.return %1 : tensor<*xf64>
# CHECK-NEXT:    }
# CHECK-NEXT:  }
