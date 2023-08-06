var spec = {
  "$schema": "https://vega.github.io/schema/vega-lite/v3.json",
  "description": "A bar chart that sorts the y-values by the x-values.",
  "width": 360,
  "height": 200,
  "data": { "url": "data?_by=Segment" },
  "mark": "bar",
  "encoding": {
    "y": {
      "field": "Segment",
      "type": "nominal",
      "sort": { "encoding": "x" },
      "axis": { "title": "Segment" }
    },
    "x": {
      "field": "Sales|sum",
      "type": "quantitative",
    }
  }
}
