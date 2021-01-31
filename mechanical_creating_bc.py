static_structural = Model.Analyses[0]

#generate mesh
Model.Mesh.GenerateMesh()

#apply fixed support
support=[x for x in Model.NamedSelections.Children if x.Name == "fixed_support"].pop()
mySupport = DataModel.AnalysisList[0].AddFixedSupport()
mySupport.Location=support
        
#apply force
force=[x for x in Model.NamedSelections.Children if x.Name == "force"].pop()
myLoad = DataModel.AnalysisList[0].AddForce()
myLoad.Location=force
myLoad.Magnitude.Output.DiscreteValues=[Quantity('1 [N]')]

#created contour stress
solution= static_structural.Solution
stress= solution.AddEquivalentStress()
solution.AddTotalDeformation()
 
#run simulation
static_structural.Solve()

#evaluate results
solution.EvaluateAllResults()

#find max stress
maximum_stress=[]
maximum_stress.append(stress.Maximum)