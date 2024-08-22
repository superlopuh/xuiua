// RUN: xuiua lower %s 'shape-inference' | filecheck %s

// CHECK:         %t = "test.op"() : () -> tensor<2x3xf64>
%t = "test.op"() : () -> tensor<2x3xf64>

// CHECK-NEXT:    %add = "uiua.add"(%t, %t) : (tensor<2x3xf64>, tensor<2x3xf64>) -> tensor<2x3xf64>
%add = "uiua.add"(%t, %t) : (tensor<2x3xf64>, tensor<2x3xf64>) -> tensor<2x3xf64>

// CHECK-NEXT:  %cast = "uiua.cast"(%t) : (tensor<2x3xf64>) -> tensor<*xf64>
%cast = "uiua.cast"(%t) : (tensor<2x3xf64>) -> tensor<*xf64>

