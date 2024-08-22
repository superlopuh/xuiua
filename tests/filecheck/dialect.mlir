// RUN: xuiua lower %s | filecheck %s

// CHECK:  %t = "test.op"() : () -> tensor<*xf64>
%t = "test.op"() : () -> tensor<*xf64>

// CHECK-NEXT:  %add = "uiua.add"(%t, %t) : (tensor<*xf64>, tensor<*xf64>) -> tensor<*xf64>
%add = "uiua.add"(%t, %t) : (tensor<*xf64>, tensor<*xf64>) -> tensor<*xf64>

// CHECK-NEXT:  %cast = "uiua.cast"(%t) : (tensor<*xf64>) -> tensor<*xf64>
%cast = "uiua.cast"(%t) : (tensor<*xf64>) -> tensor<*xf64>
