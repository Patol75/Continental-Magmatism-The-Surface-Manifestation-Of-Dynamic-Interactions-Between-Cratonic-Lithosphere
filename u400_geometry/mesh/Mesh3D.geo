height = 6.6e5;
width = 4e6;
thick = 4e6;
infDepth = 2e5;
ptcCenterX = 2.15e6;
ptcCenterY = 2e6;
ptcCenterZ = 0;
ptcOuterRadius = 2e5;
ptcInnerRadius = 5e4;

// Inner Patch
Point(1) = {ptcCenterX, ptcCenterY, ptcCenterZ};
Point(2) = {ptcCenterX + ptcInnerRadius, ptcCenterY, ptcCenterZ};
Point(3) = {ptcCenterX, ptcCenterY + ptcInnerRadius, ptcCenterZ};
Point(4) = {ptcCenterX - ptcInnerRadius, ptcCenterY, ptcCenterZ};
Point(5) = {ptcCenterX, ptcCenterY - ptcInnerRadius, ptcCenterZ};
Circle(1) = {2, 1, 3};
Circle(2) = {3, 1, 4};
Circle(3) = {4, 1, 5};
Circle(4) = {5, 1, 2};
For i In { 1 : 4 }
    Physical Line(i) = {i};
EndFor
Line Loop(1) = {1, 2, 3, 4};
Plane Surface(1) = {1};
Physical Surface(1) = {1};
// Outer Patch
Point(6) = {ptcCenterX + ptcOuterRadius, ptcCenterY, ptcCenterZ};
Point(7) = {ptcCenterX, ptcCenterY + ptcOuterRadius, ptcCenterZ};
Point(8) = {ptcCenterX - ptcOuterRadius, ptcCenterY, ptcCenterZ};
Point(9) = {ptcCenterX, ptcCenterY - ptcOuterRadius, ptcCenterZ};
Circle(5) = {6, 1, 7};
Circle(6) = {7, 1, 8};
Circle(7) = {8, 1, 9};
Circle(8) = {9, 1, 6};
For i In { 5 : 8 }
    Physical Line(i) = {i};
EndFor
Line Loop(2) = {5, 6, 7, 8};
Plane Surface(2) = {2, 1};
Physical Surface(2) = {2};

// Front Face (Y == 0)
Point(10) = {0, 0, height};
Point(11) = {width, 0, height};
Point(12) = {width, 0, height - infDepth};
Point(13) = {width, 0, 0};
Point(14) = {0, 0, 0};
Point(15) = {0, 0, height - infDepth};
Line(9) = {10, 11};
Line(10) = {15, 12};
Line(11) = {14, 13};
Line(12) = {11, 12};
Line(13) = {12, 13};
Line(14) = {14, 15};
Line(15) = {15, 10};
For i In { 9 : 15 }
    Physical Line(i) = {i};
EndFor
Line Loop(3) = {9, 12, -10, 15};
Line Loop(4) = {10, 13, -11, 14};
For i In { 3 : 4 }
    Plane Surface(i) = {i};
    Physical Surface(i) = {i};
EndFor
// Back Face (Y == thick)
Point(16) = {0, thick, height};
Point(17) = {width, thick, height};
Point(18) = {width, thick, height - infDepth};
Point(19) = {width, thick, 0};
Point(20) = {0, thick, 0};
Point(21) = {0, thick, height - infDepth};
Line(16) = {16, 17};
Line(17) = {21, 18};
Line(18) = {20, 19};
Line(19) = {17, 18};
Line(20) = {18, 19};
Line(21) = {20, 21};
Line(22) = {21, 16};
For i In { 16 : 22 }
    Physical Line(i) = {i};
EndFor
Line Loop(5) = {16, 19, -17, 22};
Line Loop(6) = {17, 20, -18, 21};
For i In { 5 : 6 }
    Plane Surface(i) = {i};
    Physical Surface(i) = {i};
EndFor
// Right Face (X == width)
Line(23) = {11, 17};
Line(24) = {12, 18};
Line(25) = {13, 19};
For i In { 23 : 25 }
    Physical Line(i) = {i};
EndFor
Line Loop(7) = {23, 19, -24, -12};
Line Loop(8) = {24, 20, -25, -13};
For i In { 7 : 8 }
    Plane Surface(i) = {i};
    Physical Surface(i) = {i};
EndFor
// Left Face (X == 0)
Line(26) = {10, 16};
Line(27) = {15, 21};
Line(28) = {14, 20};
For i In { 26 : 28 }
    Physical Line(i) = {i};
EndFor
Line Loop(9) = {26, -22, -27, 15};
Line Loop(10) = {27, -21, -28, 14};
For i In { 9 : 10 }
    Plane Surface(i) = {i};
    Physical Surface(i) = {i};
EndFor
// Top Face (Z == height)
Line Loop(11) = {9, 23, -16, -26};
Plane Surface(11) = {11};
Physical Surface(11) = {11};
// Bottom Face (Z == 0)
Line Loop(12) = {11, 25, -18, -28};

Plane Surface(12) = {12, 2};
Physical Surface(12) = {12};

// Whole Domain

Surface Loop(1) = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
Volume(1) = {1};
Physical Volume(1) = {1};

Field[1] = Box;
Field[1].VIn = 15e3;
Field[1].VOut = 2e5;
Field[1].XMin = 0;
Field[1].XMax = width;
Field[1].YMin = 0;
Field[1].YMax = thick;
Field[1].ZMin = 4.6e5;
Field[1].ZMax = height;

Field[2] = Box;
Field[2].VIn = 15e3;
Field[2].VOut = 2e5;
Field[2].XMin = ptcCenterX - ptcOuterRadius;
Field[2].XMax = ptcCenterX + ptcOuterRadius;
Field[2].YMin = ptcCenterY - ptcOuterRadius;
Field[2].YMax = ptcCenterY + ptcOuterRadius;
Field[2].ZMin = 0;
Field[2].ZMax = 5e4;

Field[3] = Min;
Field[3].FieldsList = {1, 2};

Background Field = 3;
