# RUN: xuiua lower %s 'add-shapes{shapes="Sum=2x3"}' | filecheck %s
# ,shape-inference,remove-casts,convert-uiua-to-stablehlo

Sum ← /+

# CHECK:       builtin.module {
# CHECK-NEXT:    func.func @Sum(%0 : tensor<2x3xf64>) -> tensor<*xf64> {
# CHECK-NEXT:      %1 = "uiua.reduce"(%0) ({
# CHECK-NEXT:      ^0(%2 : tensor<*xf64>, %3 : tensor<*xf64>):
# CHECK-NEXT:          %4 = "uiua.add"(%2, %3) : (tensor<*xf64>, tensor<*xf64>) -> tensor<*xf64>
# CHECK-NEXT:          "uiua.yield"(%4) : (tensor<*xf64>) -> ()
# CHECK-NEXT:      }) : (tensor<2x3xf64>) -> tensor<*xf64>
# CHECK-NEXT:      %5 = "uiua.cast"(%1) : (tensor<*xf64>) -> tensor<*xf64>
# CHECK-NEXT:      func.return %5 : tensor<*xf64>
# CHECK-NEXT:    }
# CHECK-NEXT:  }
