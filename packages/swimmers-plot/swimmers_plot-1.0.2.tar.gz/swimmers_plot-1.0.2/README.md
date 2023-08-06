# swimmers_plot
Create a swimmer's plot of treatments for a cohort

To install:

`pip install swimmers-plot`

To use:

```
import swimmers_plot
cohort = swimmers_plot.Cohort()
cohort.load_samples('sample_inp.tsv')
cohort.load_treatments('treatment_inp.tsv')
cohort.make_swimmers_plot()
```
