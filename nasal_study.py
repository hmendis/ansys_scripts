# Created by Hashan Mendis from LEAP Australia 2018
# contact me on hashan.mendis@leapaust.com.au or landline 85427820
# for more information about writing scripts watch this link : https://www.youtube.com/watch?v=VbYud9l7X0I&list=PLvsJbyBB0CMcLcnFTUJox3V0ib82t4drw&index=11


# required to start fluent from this python script
import os
import subprocess

#-------CHANGE VALUES BELOW THIS LINE-------
# factors array will multiply the max face size with the factor ie (define face-max (* 2 factor))
# for mesh study that reduces the mesh by 20% :factors = [1,0.8,0.6]
factors = [1,2,3,4]

# for documentation
study = "mesh_test"
filename = "MRI_CRS_2"
initials = "hm"
iterations = "500"
flowrate = "0.0001755"

#meshing commands to change tet,poly,hexcore,polyhecore
mesh = "poly"

# path needed if you want to run fluent from this script
path = "C:\\Program Files\\ANSYS Inc\\v194\\fluent\\ntbin\\win64\\fluent"
precision = "3ddp"
core = 36

# initilise how many cases are created according to the number of factors
case = list(range(1,(len(factors)+1)))
count = 0

#-------CHANGE VALUES ABOVE THIS LINE-------

#commands below change the mesh type as long as prism are created
if (mesh == "tet"):
    meshstudy = (";meshing tet\n"
                 "mesh tet controls cell-sizing size-field\n"
                 "mesh auto-mesh * no scoped pyramids tet yes")
elif (mesh == "poly"):
    meshstudy = (";meshing poly\n"
                 "mesh poly controls cell-sizing size-field\n"
                 "mesh auto-mesh * no scoped pyramids poly yes")
elif (mesh == "hexcore"):
    meshstudy = (";meshing hexcore\n"
                 "mesh hexcore controls octree-hexcore? yes\n"
                 "mesh auto-mesh * no scoped pyramids hexcore yes")
elif (mesh == "polyhexcore"):
    meshstudy = (";meshing polyhexcore\n"
                 "mesh auto-mesh * no scoped pyramids poly-hexcore yes")
else:
	meshstudy = (";issue with mesh variable so printing tet\n"
                 "mesh tet controls cell-sizing size-field\n"
                 "mesh auto-mesh * no scoped pyramids tet yes")

# following creates the journal
script_temp="""
;------- CHANGE THIS SECTION BELOW -------

;{7}_case_{2}_{8}_{5} script
(define study "{7}_case_{2}_{8}_{5}")
(define factor {0})
(define fileName "{1}")

;;transcript
(ti-menu-load-string (format #f "file start-transcript ~a-~a-~02d.trn" study fileName factor))

;;define global parameters
(define global-min 0.2)
(define global-max(/ 3.2 factor))
(define global-growth-rate 1.2)

;;surface mesh
(define face-min 0.8)
(define norm-angle 18)
(define cells-per-gap 1)
;hexcore - 0.1,0.2,0.4,0.8,1.6,3.2

;;prism layers
(define first-layer-height 0.1)
(define number-of-layers 5)
(define last-percent 20)

;------- CHANGE THIS SECTION ABOVE -------

;------- FLUENT MESHING -------

;;import cad faceting
/file import cad-options save-PMDB? yes
(ti-menu-load-string (format #f "/file import cad , ~a.stl , , , mm" fileName))

;;define global size-functions
/size-functions set-global-controls global-min global-max global-growth-rate

;;create sizing
/scoped-sizing create face-zones-b curvature face-zone yes no b* face-min global-max global-growth-rate norm-angle
/scoped-sizing create face-zones-c curvature face-zone yes no c* face-min global-max global-growth-rate norm-angle
/scoped-sizing create face-zones-extension curvature face-zone yes no extension* face-min global-max global-growth-rate norm-angle

/scoped-sizing create face-zones-prox-b proximity face-zone yes no b* face-min global-max global-growth-rate cells-per-gap both no yes
/scoped-sizing create face-zones-prox-c proximity face-zone yes no c* face-min global-max global-growth-rate cells-per-gap both no yes

;;compute size field
/scoped-sizing compute

;;creating a material point
/material-point create-material-point material-point-in -4.935824 -116.621407 -51.390686

;;extract edges
/objects extract-edges (*) feature 40

;;extract intersection loops
/objects create-intersection-loops collectively (*)

;;wrap objects
/objects wrap wrap (*) collectively fluid shrink-wrap material-point-in hybrid 0.7

;;write mesh for de-bugging
(ti-menu-load-string (format #f "/file write-mesh mesh-wrap-section-~a-~a-~02d.msh.gz" study fileName factor))

;;delete geometry objects
/objects delete-all-geom

;;/diagnostics quality improve
/diagnostics quality general-improve objects (*) skewness 0.95 40 30 yes
/diagnostics quality general-improve objects (*) skewness 0.9 40 30 yes
/diagnostics quality general-improve objects (*) skewness 0.8 40 30 yes
/diagnostics quality general-improve objects (*) skewness 0.7 40 30 yes
/diagnostics quality general-improve objects (*) skewness 0.6 40 30 yes
/diagnostics quality general-improve objects (*) skewness 0.5 40 30 yes

/diagnostics quality collapse objects (*) skewness 0.99 40 30 no
/diagnostics quality collapse objects (*) skewness 0.98 40 30 no
/diagnostics quality collapse objects (*) skewness 0.96 40 30 no
/diagnostics quality collapse objects (*) skewness 0.94 40 30 no
/diagnostics quality collapse objects (*) skewness 0.92 40 30 no
/diagnostics quality collapse objects (*) skewness 0.9 40 30 no

/diagnostics quality general-improve objects (*) skewness 0.95 40 30 yes
/diagnostics quality general-improve objects (*) skewness 0.9 40 30 yes
/diagnostics quality general-improve objects (*) skewness 0.8 40 30 yes
/diagnostics quality general-improve objects (*) skewness 0.7 40 30 yes
/diagnostics quality general-improve objects (*) skewness 0.6 40 30 yes
/diagnostics quality general-improve objects (*) skewness 0.5 40 30 yes

/diagnostics quality collapse objects (*) skewness 0.99 40 30 no
/diagnostics quality collapse objects (*) skewness 0.98 40 30 no
/diagnostics quality collapse objects (*) skewness 0.96 40 30 no
/diagnostics quality collapse objects (*) skewness 0.94 40 30 no
/diagnostics quality collapse objects (*) skewness 0.92 40 30 no
/diagnostics quality collapse objects (*) skewness 0.9 40 30 no

/diagnostics quality general-improve objects (*) skewness 0.95 40 30 yes
/diagnostics quality general-improve objects (*) skewness 0.9 40 30 yes
/diagnostics quality general-improve objects (*) skewness 0.8 40 30 yes
/diagnostics quality general-improve objects (*) skewness 0.7 40 30 yes
/diagnostics quality general-improve objects (*) skewness 0.6 40 30 yes
/diagnostics quality general-improve objects (*) skewness 0.5 40 30 yes

;;volume mesh
/objects volumetric-regions compute * no
/objects vol-reg change-type * (*) fluid

;;create volume mesh
/mesh scoped-prisms create prism-nasal-b last-ratio first-layer-height number-of-layers last-percent fluid fluid-regions selected-face-zones b*
/mesh scoped-prisms create prism-nasal-c last-ratio first-layer-height number-of-layers last-percent fluid fluid-regions selected-face-zones c*
/mesh scoped-prisms create prism-nasal-extension last-ratio first-layer-height number-of-layers last-percent fluid fluid-regions selected-face-zones extension*

{6}

;;volume mesh /diagnostics
/mesh modify auto-node-move (*) (*) 0.99 50 120 yes 10
/mesh modify auto-node-move (*) (*) 0.98 50 120 yes 10
/mesh modify auto-node-move (*) (*) 0.96 50 120 yes 10
/mesh modify auto-node-move (*) (*) 0.94 50 120 yes 10
/mesh modify auto-node-move (*) (*) 0.92 50 120 yes 10
/mesh modify auto-node-move (*) (*) 0.90 50 120 yes 10

;;volume mesh /diagnostics
/mesh check-quality

;;write mesh for de-bugging
(ti-menu-load-string (format #f "/file write-mesh mesh-before-solution-~a-~a~02d.msh.gz" study fileName factor))

;;scale down
/objects scale (*) 0.001 0.001 0.001

;;prepare mesh to solve
/mesh prepare-for-solve yes

;;switch to solution
/switch-to-solution-mode yes

;------- FLUENT SOLVER -------

;------- CHANGE THIS SECTION BELOW -------
;;define variables
(define flow {4})
(define number-of-iterate {3})

;{7}_case_{2}_{8}_{5} script
(define study "{7}_case_{2}_{8}_{5}")
(define factor {0})
(define fileName "{1}")

;------- CHANGE THIS SECTION ABOVE -------

;;file save settings
/file hdf-files? yes
/file set-batch-options yes no yes no

;;define zone types
/define boundary-conditions modify-zones zone-type (a_external-front) pressure-inlet
/define boundary-conditions modify-zones zone-type (outlet) mass-flow-outlet

;;define boundary conditions
/define boundary-conditions mass-flow-outlet outlet yes yes no flow

;;not checking residuals
/solve monitors residual criterion-type 3

;;setting time scales
/solve set pseudo-transient yes yes 1 0.01 0

;;set up monitor points for total pressure
/solve report-definitions add pressure-drop-outlet surface-areaavg field total-pressure surface-names (outlet) q
/solve report-plots add pressure-drop-outlet-plot report-defs (pressure-drop-outlet) q
/solve report-files add monitor-point-summary report-defs (pressure-drop-outlet) q
(ti-menu-load-string (format #f "/solve report-files edit monitor-point-summary file-name report-~a-~a-~02d.csv q" study fileName factor))

;;write
(ti-menu-load-string (format #f "/file write-case before-run-~a-~a-~02d" study fileName factor))

;;initialize
/solve initialize initialize-flow
/solve initialize fmg-initialization yes

;;solve
(benchmark '(iterate number-of-iterate))

;;report
/report system proc-stats
/report system time-stats
(ti-menu-load-string (format #f "report summary yes summary-~a-~a-~02d" study fileName factor))

;;create new plane and export data
/surface plane-point-n-normal y=0.07 0.00712338 -0.0799227 -0.0527844 5.5e-08 0.7029 0.7112
/file export ascii plane-y=0.07.csv y=0.07 () yes velocity-magnitude pressure () yes

/surface plane-point-n-normal y=0.06 0.00911082 -0.0672016 -0.0495219 5.5e-08 0.9995 0.0319
/file export ascii plane-y=0.06.csv (y=0.06) yes velocity-magnitude pressure () yes

/surface plane-point-n-normal y=0.04 0.00983956 -0.0466045 -0.0464198 0 1 0
/file export ascii plane-y=0.04.csv (y=0.04) yes velocity-magnitude pressure () yes

/surface plane-point-n-normal y=0.01 0.01435124 -0.0117738 -0.0617434 -3.1e-07 0.9084 -0.418
/file export ascii plane-y=0.01.csv (y=0.01) yes velocity-magnitude pressure () yes

/surface plane-point-n-normal y=0.03 0.02974304 -0.0306614 -0.0505425 0 1 0
/file export ascii plane-y=0.03.csv (y=0.03) yes velocity-magnitude pressure () yes

/surface plane-point-n-normal y=0.008 0.01471462 0.00080386 -0.1209135 0 0 1
/file export ascii plane-y=0.008.csv (y=0.008) yes velocity-magnitude pressure () yes

;;report total pressure
/report surface-integrals area-weighted-avg (outlet) total-pressure yes total-pressure-outlet.txt

;;write
(ti-menu-load-string (format #f "/file write-case-data solved-~a-~a-~02d" study fileName factor))

;;close transcript
/file stop-transcript

exit
"""

# creates multiple jorunal files
for factor in factors:
    jou_file_name = "{5}_{0}_{1}_{4}_factor_{2}_{3}.jou".format(filename, study, factor, initials, mesh, case[count])
    with open(jou_file_name, 'wt') as jou_file:
        jou_file.write(script_temp.format(factor, filename, study, iterations, flowrate, initials, meshstudy, case[count], mesh))
    count += 1
