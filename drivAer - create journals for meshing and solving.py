import os
import subprocess

factors = [1,0]
study = "mesh_testing"
filename = "drivaer"
initials = "hm"
iterations = "10"
velocity = "20"

path = "C:\\Program Files\\ANSYS Inc\\v191\\fluent\\ntbin\\win64\\fluent"
precision = "3ddp"
core = 4

case = list(range(1,(len(factors)+1)))
count = 0

#meshing commands tet,poly,hexcore,polyhecore
mesh = "polyhexcore"

if (mesh == "tet"):
    meshstudy = (";meshing tet\n"
                 "mesh tet controls cell-sizing size-field\n"
                 "mesh auto-mesh en* no scoped pyramids tet yes")
elif (mesh == "poly"):
    meshstudy = (";meshing poly\n"
                 "mesh poly controls cell-sizing size-field\n"
                 "mesh auto-mesh * no scoped pyramids poly yes")
elif (mesh == "hexcore"):
    meshstudy = (";meshing hexcore\n"
                 "mesh hexcore controls octree-hexcore? yes\n"
                 "mesh auto-mesh en* no scoped pyramids hexcore yes")
elif (mesh == "polyhexcore"):
    meshstudy = (";meshing polyhexcore\n"
                 "mesh auto-mesh * no scoped pyramids poly-hexcore yes")
else:
	meshstudy = (";issue with mesh variable so printing tet\n"
                 "mesh tet controls cell-sizing size-field\n"
                 "mesh auto-mesh en* no scoped pyramids tet yes")

script_temp="""
;------- CHANGE THIS SECTION BELOW -------

;{7}_case_{2}_{5} script
(define study "{7}_case_{2}_{5}")
(define factor {0})
(define fileName "{1}")

;;transcript
(ti-menu-load-string (format #f "file start-transcript ~a-~a-~02d.trn" study fileName factor))

;Name selection wing
;Volume selection : enclosure, boi-1, boi-2
;Name selection on enclosure : inlet, outlet, wall, symmetry, car

;;define global parameters
(define global-min 0.3)
(define global-max 160)
(define global-growth-rate 1.2)

;;define car parameters
(define min-face-size-car 0.3)
(define max-face-size-car 50)

(define norm-angle 9)
(define cells-per-gap 4)

;;define boi parameters
(define boi-1 32)
(define boi-2 64)

;prism
(define first-layer-height 0.1)
(define number-of-layers 6)
(define last-percent 20)

;rotation
(define yaw-angle 5)
(define pitch-angle 1)
(define roll-angle 2)

;domain size
(define wake-length 4000)

;------- CHANGE THIS SECTION ABOVE -------

;------- FLUENT MESHING -------

;beta functions
beta-feature-access yes yes

;;import cad faceting
/file import cad-options save-PMDB? yes
(ti-menu-load-string (format #f "file import cad , ~a.scdoc , , , mm" fileName))

;create domain
/boundary create-bounding-box (*) wall domain 500 absolute -2000 0 -2000 wake-length 2000 2000 yes
/boundary create-bounding-box (*) wall boi-1 250 absolute -300 0 -750 wake-length 500 750 yes

;change domain face names
/boundary manage name domain-xmin velocity-inlet
/boundary manage name domain-xmax pressure-outlet
/boundary manage name domain-ymin ground
/boundary manage name domain-ymax y-max-wall
/boundary manage name domain-zmax z-max-wall
/boundary manage name domain-zmin z-min-wall

;rotate the geometry object component
;/objects rotate wheel* (*wing*) yaw-angle 0 1 0 0 0 0
;/objects rotate (*wing*) pitch-angle 0 0 1 0 0 0
;/objects rotate (*wing*) roll-angle 1 0 0 0 0 0

;;define global size-functions
/size-functions set-global-controls global-min global-max global-growth-rate

;;create sizing
/scoped-sizing create face-zones-curv-car curvature face-zone yes no car* min-face-size-car max-face-size-car global-growth-rate norm-angle
/scoped-sizing create face-zones-prox-car proximity face-zone yes no car* min-face-size-car max-face-size-car global-growth-rate cells-per-gap both no yes
/scoped-sizing create boi-1 boi object-faces-and-edges yes no boi-1* boi-1 global-growth-rate
;/scoped-sizing create boi-2 boi object-faces-and-edges yes no boi-2* boi-2 global-growth-rate

;;compute size field
/scoped-sizing compute
(ti-menu-load-string (format #f "file write-size-field ~a-~02d.sizing" fileName factor))

;;creating a material point
/material-point create-material-point material-point-in 0 1000 0

;;extract edges
/objects extract-edges (*) feature 40

;;extract intersection loops
/objects create-intersection-loops collectively (*)

;;wrap objects
/objects wrap wrap *w* (*d*) collectively internal-mesh shrink-wrap material-point-in hybrid 0.7

;;improve features
/objects improve-feature-capture (*) 3 0

;write mesh for de-bugging
(ti-menu-load-string (format #f "file write-mesh mesh-wrap-section-~a-~a-~02d.msh.gz" study fileName factor))

;;diagnostics free faces
;/diagnostics face-connectivity fix-free-faces face-zones (*) merge-nodes y 10
;/diagnostics face-connectivity fix-free-faces face-zones (*) merge-nodes y 20
;/diagnostics face-connectivity fix-free-faces face-zones (*) merge-nodes y 30
;/diagnostics face-connectivity fix-free-faces face-zones (*) stitch 0.05 5
;/diagnostics face-connectivity fix-free-faces face-zones (*) stitch 0.1 5

;;diagnostics multi
;/diagnostics face-connectivity fix-multi-faces face-zones (*) all-above 5 20 20

;write mesh for de-bugging
(ti-menu-load-string (format #f "file write-mesh mesh-after-import-~a-~a-~02d.msh.gz" study fileName factor))

;;diagnostics quality improve
/diagnostics quality general-improve objects (en*) skewness 0.95 40 30 yes
/diagnostics quality general-improve objects (en*) skewness 0.9 40 30 yes
/diagnostics quality general-improve objects (en*) skewness 0.8 40 30 yes
/diagnostics quality general-improve objects (en*) skewness 0.7 40 30 yes
/diagnostics quality general-improve objects (en*) skewness 0.6 40 30 yes
/diagnostics quality general-improve objects (en*) skewness 0.5 40 30 yes

/diagnostics quality collapse objects (en*) skewness 0.99 40 30 no
/diagnostics quality collapse objects (en*) skewness 0.98 40 30 no
/diagnostics quality collapse objects (en*) skewness 0.97 40 30 no
/diagnostics quality collapse objects (en*) skewness 0.96 40 30 no
/diagnostics quality collapse objects (en*) skewness 0.95 40 30 no
/diagnostics quality collapse objects (en*) skewness 0.9 40 30 no
/diagnostics quality collapse objects (en*) skewness 0.85 40 30 no

/diagnostics quality general-improve objects (en*) skewness 0.95 40 30 yes
/diagnostics quality general-improve objects (en*) skewness 0.9 40 30 yes
/diagnostics quality general-improve objects (en*) skewness 0.8 40 30 yes
/diagnostics quality general-improve objects (en*) skewness 0.7 40 30 yes
/diagnostics quality general-improve objects (en*) skewness 0.6 40 30 yes
/diagnostics quality general-improve objects (en*) skewness 0.5 40 30 yes

/diagnostics quality general-improve objects (en*) skewness 0.95 40 30 yes
/diagnostics quality general-improve objects (en*) skewness 0.9 40 30 yes
/diagnostics quality general-improve objects (en*) skewness 0.8 40 30 yes
/diagnostics quality general-improve objects (en*) skewness 0.7 40 30 yes
/diagnostics quality general-improve objects (en*) skewness 0.6 40 30 yes
/diagnostics quality general-improve objects (en*) skewness 0.5 40 30 yes

;;volume mesh
/objects volumetric-regions compute * no
/objects vol-reg change-type * (*) fluid

;;create volume mesh
mesh scoped-prisms create prism-car last-ratio first-layer-height number-of-layers last-percent (*) fluid-regions selected-face-zones car*

{6}

;;change types
boundary manage type (*outlet*) pressure-outlet
boundary manage type (*inlet*) velocity-inlet

;;volume mesh /diagnostics
mesh modify auto-node-move (*) (*) 0.99 50 120 yes 10
mesh modify auto-node-move (*) (*) 0.98 50 120 yes 10
mesh modify auto-node-move (*) (*) 0.96 50 120 yes 10
mesh modify auto-node-move (*) (*) 0.94 50 120 yes 10
mesh modify auto-node-move (*) (*) 0.92 50 120 yes 10
mesh modify auto-node-move (*) (*) 0.90 50 120 yes 10

;;volume mesh /diagnostics
mesh check-quality

;write mesh for de-bugging
(ti-menu-load-string (format #f "file write-mesh mesh-before-solution-~a-~a~02d.msh.gz" study fileName factor))

;;scale down
mesh manage scale-model 0.001 0.001 0.001

;;prepare mesh to solve
mesh prepare-for-solve yes

;;switch to solution
/switch-to-solution-mode yes yes

;------- FLUENT SOLVER -------

;------- CHANGE THIS SECTION BELOW -------

;{7}_case_{2}_{5} script
(define study "{7}_case_{2}_{5}")
(define factor {0})
(define fileName "{1}")

;;define variables
(define velocity {4})
(define number-of-iterate {3})

;front wheel parameters
;(w=v/r)
(define radius 0.2)
(define wheel-rot-speed (/ air-speed radius))
(define x-pos-wheel 0.76)
(define y-pos-wheel 0.192)
(define z-pos-wheel 0)
(define x-comp-wheel 0)
(define y-comp-wheel 0)
(define z-comp-wheel 1)

;------- CHANGE THIS SECTION ABOVE -------

;;file save settings
file hdf-files? yes

;;model type
;/define models viscous kw-sst? yes
/define models viscous kw-geko? yes
/define models viscous curvature-correction? yes

;;message from fluent
/display set nodewt-based-interp? no

;;define zone types
/define boundary-conditions modify-zones zone-type enclosure fluid
/define boundary-conditions modify-zones zone-type inlet velocity-inlet
/define boundary-conditions modify-zones zone-type outlet pressure-outlet
/define boundary-conditions modify-zones zone-type symmetry symmetry

;;define boundary conditions
/define boundary-conditions wall wall yes motion-bc-moving , , no , , air-speed 1 0 0 , , , , ,
/define boundary-conditions wall ground yes motion-bc-moving , , no , , air-speed 1 0 0 , , , , ,
/define boundary-conditions velocity-inlet inlet no no yes yes no air-speed no 0 no no yes 5 10
/define boundary-conditions pressure-outlet outlet yes no 0 no yes no no yes 5 10 no yes no yes no
/define boundary-conditions wall wheel_left yes motion-bc-moving no no yes no no 0 no 0.5 no wheel-rot-speed x-pos-wheel y-pos-wheel z-pos-wheel x-comp-wheel y-comp-wheel z-comp-wheel
/define boundary-conditions copy-bc wheel_left (wheel_right)


;;set methods conditions
/solve set p-v-coupling 24
/solve set pseudo-transient yes yes 1 1 1
/solve set warped-face-gradient-correction enable? yes yes
/solve set high-order-term-relaxation enable yes
/solve set discretization-scheme pressure 14
/solve set discretization-scheme k 4
/solve set discretization-scheme mom 4
/solve set discretization-scheme omega 4

;;write
(ti-menu-load-string (format #f "file write-case before-run-~a-~a-~02d" study fileName factor))

;;increase residuals
/solve monitors residual convergence-criteria 0.0001 0.0001 0.0001 0.0001 0.0001 0.0001

;;set up monitor points
/solve report-definitions add x-car force force-vector 1 0 0 thread-ids (car) quit
/solve report-plots add x-plot report-defs (x-car) quit

/solve report-definitions add y-car force force-vector 0 1 0 thread-ids (frontcar) quit
/solve report-plots add y-plot report-defs (y-car) quit

;set up reports
/solve report-files add monitor-point-summary frequency 1 report-defs x-car (y-car) quit
/solve report-files edit monitor-point-summary print? yes
(ti-menu-load-string (format #f "solve report-files edit monitor-point-summary file-name report-~a-~a-~02d.csv" study fileName factor))

;;initialize
solve initialize initialize-flow
solve initialize fmg-initialization yes

;;solve
(benchmark '(iterate number-of-iterate))
(ti-menu-load-string (format #f "plot residuals-set plot-to-file residuals-~a-~a-~02d.csv" study fileName factor))
/solve iterate 1

;;report
/report system proc-stats
/report system time-stats
(ti-menu-load-string (format #f "report summary yes summary-~a-~a-~02d" study fileName factor))

;;write
(ti-menu-load-string (format #f "file write-case-data solved-~a-~a-~02d" study fileName factor))

;close transcript
/file stop-transcript ok

exit
"""

for factor in factors:
    jou_file_name = "{5}_{0}_{1}_{4}_factor_{2}_{3}.jou".format(filename, study, factor, initials, mesh, case[count])
    with open(jou_file_name, 'wt') as jou_file:
        jou_file.write(script_temp.format(factor, filename, study, iterations, velocity, initials, meshstudy, case[count]))
