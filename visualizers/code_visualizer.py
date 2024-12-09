import json
import os

class CodeVisualizer:
    """Generates interactive visualizations using D3.js."""
    def __init__(self, analysis_results):
        self.analysis_results = analysis_results
        self.output_file = 'visualization.html'

    def generate_visualizations(self):
        data = self._prepare_data()
        html_content = self._generate_html(data)
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def _prepare_data(self):

        nodes = []
        links = []
        for result in self.analysis_results:
            file_node = {"id": result["file"], "group": 1}
            nodes.append(file_node)
            for func in result["complexity_metrics"].get("functions", []):
                func_node = {"id": func, "group": 2}
                nodes.append(func_node)
                links.append({"source": result["file"], "target": func, "value": 1})
        return {"nodes": nodes, "links": links}

    def _generate_html(self, data):

        data_json = json.dumps(data)
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Code Analysis Visualization</title>
            <style>
                .node {{
                    stroke: #fff;
                    stroke-width: 1.5px;
                }}
                .link {{
                    stroke: #999;
                    stroke-opacity: 0.6;
                }}
            </style>
        </head>
        <body>
        <script src="https://d3js.org/d3.v5.min.js"></script>
        <script>
            var data = {data_json};

            var width = 960,
                height = 600;

            var svg = d3.select("body").append("svg")
                .attr("width", width)
                .attr("height", height);

            var simulation = d3.forceSimulation()
                .force("link", d3.forceLink().id(function(d) {{ return d.id; }}))
                .force("charge", d3.forceManyBody())
                .force("center", d3.forceCenter(width / 2, height / 2));

            var link = svg.append("g")
                .attr("class", "links")
              .selectAll("line")
              .data(data.links)
              .enter().append("line")
                .attr("stroke-width", function(d) {{ return Math.sqrt(d.value); }});

            var node = svg.append("g")
                .attr("class", "nodes")
              .selectAll("circle")
              .data(data.nodes)
              .enter().append("circle")
                .attr("r", 5)
                .attr("fill", function(d) {{ return d.group === 1 ? "blue" : "green"; }})
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));

            node.append("title")
                .text(function(d) {{ return d.id; }});

            simulation
                .nodes(data.nodes)
                .on("tick", ticked);

            simulation.force("link")
                .links(data.links);

            function ticked() {{
                link
                    .attr("x1", function(d) {{ return d.source.x; }})
                    .attr("y1", function(d) {{ return d.source.y; }})
                    .attr("x2", function(d) {{ return d.target.x; }})
                    .attr("y2", function(d) {{ return d.target.y; }});

                node
                    .attr("cx", function(d) {{ return d.x; }})
                    .attr("cy", function(d) {{ return d.y; }});
            }}

            function dragstarted(d) {{
                if (!d3.event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            }}

            function dragged(d) {{
                d.fx = d3.event.x;
                d.fy = d3.event.y;
            }}

            function dragended(d) {{
                if (!d3.event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            }}
        </script>
        </body>
        </html>
        """
        return html_template