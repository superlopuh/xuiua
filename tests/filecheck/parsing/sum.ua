# RUN: xuiua lower %s 'add-shapes{shapes="Sum=2x3"},shape-inference,remove-casts,convert-uiua-to-stablehlo' | filecheck %s

Sum ← /+

# CHECK:       builtin.module {
# CHECK-NEXT:    func.func @Sum(%0 : tensor<2x3xf64>) -> tensor<3xf64> {
# CHECK-NEXT:      %1 = arith.constant dense<0.000000e+00> : tensor<f64>
# CHECK-NEXT:      %2 = "stablehlo.reduce"(%0, %1) ({
# CHECK-NEXT:      ^0(%3 : tensor<f64>, %4 : tensor<f64>):
# CHECK-NEXT:          %5 = "stablehlo.add"(%3, %4) : (tensor<f64>, tensor<f64>) -> tensor<f64>
# CHECK-NEXT:          "stablehlo.return"(%5) : (tensor<f64>) -> ()
# CHECK-NEXT:      }) {"dimensions" = array<i64: 0>} : (tensor<2x3xf64>, tensor<f64>) -> tensor<3xf64>
# CHECK-NEXT:      func.return %2 : tensor<3xf64>
# CHECK-NEXT:    }
# CHECK-NEXT:  }
