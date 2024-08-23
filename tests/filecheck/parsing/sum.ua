# RUN: xuiua lower %s 'add-shapes{shapes="Sum=2x3"},shape-inference,remove-casts' | filecheck %s
# convert-uiua-to-stablehlo

Sum ← /+

# CHECK:       builtin.module {
# CHECK-NEXT:    func.func @Sum(%0 : tensor<2x3xf64>) -> tensor<3xf64> {
# CHECK-NEXT:      %1 = "uiua.reduce"(%0) ({
# CHECK-NEXT:      ^0(%2 : tensor<3xf64>, %3 : tensor<3xf64>):
# CHECK-NEXT:          %4 = "uiua.add"(%2, %3) : (tensor<3xf64>, tensor<3xf64>) -> tensor<3xf64>
# CHECK-NEXT:          "uiua.yield"(%4) : (tensor<3xf64>) -> ()
# CHECK-NEXT:      }) : (tensor<2x3xf64>) -> tensor<3xf64>
# CHECK-NEXT:      func.return %1 : tensor<3xf64>
# CHECK-NEXT:    }
# CHECK-NEXT:  }
