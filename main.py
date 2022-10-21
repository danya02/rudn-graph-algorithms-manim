from re import M
from manim import *

X = '\infty'
graph = [
    [X, 1, 3, X],
    [2, X, 3, 2],
    [X, X, X, 1],
    [X, 1, X, X]
]
MIN_WEIGHT = float('inf')
MAX_WEIGHT = 0
for i in range(len(graph)):
    for j in range(len(graph[i])):
        if graph[i][j] != X:
            MIN_WEIGHT = min(MIN_WEIGHT, graph[i][j])
            MAX_WEIGHT = max(MAX_WEIGHT, graph[i][j])

class FloydWarshall(Scene):
    def construct(self):
        global graph

        VERT_NAMES = ["V_"+str(i+1) for i in range(len(graph))]
        init_edges = []
        init_edges_conf = dict()
        grad = color_gradient([PURE_RED, PURE_GREEN], MAX_WEIGHT - MIN_WEIGHT + 1)
        for i in range(len(graph)):
            for j in range(len(graph)):
                if graph[j][i] != X:
                    init_edges.append( (f"V_{j+1}", f"V_{i+1}") )
                    init_edges_conf[(f"V_{j+1}", f"V_{i+1}")] = {
                        "stroke_color": grad[ graph[j][i] - MIN_WEIGHT ],
                    }

        initial_graph = Graph(VERT_NAMES, init_edges, edge_config=init_edges_conf, layout='circular', edge_type=Arrow)
        self.play(Create(initial_graph))
        self.wait(3)
        self.play(Uncreate(initial_graph))

        graph_labels_left = VGroup()
        graph_labels_top = VGroup()
        for i in range(len(graph)):
            graph_labels_left.add(MathTex("V_{" + f'{i+1}' + "}").scale(0.7))
            graph_labels_top.add(MathTex("V_{" + f'{i+1}' + "}").scale(0.7))

        graph_labels_left.arrange(DOWN)
        graph_labels_top.arrange(RIGHT)

        mat = Matrix(graph)
        for label, row in zip(graph_labels_left, mat.get_rows()):
            label.next_to(mat, LEFT).match_y(row) 
        for label, col in zip(graph_labels_top, mat.get_columns()):
            label.next_to(mat, UP).match_x(col)

        self.play(LaggedStartMap(Write, [mat, graph_labels_left, graph_labels_top]))
        self.wait()

        # Add "\usepackage[russian]{babel}" to preamble
        template = TexTemplate()
        new_template = TexTemplate(
            tex_compiler=template.tex_compiler,
            output_format=template.output_format,
            documentclass=template.documentclass,
            preamble=template.preamble.replace(r"english", r"russian"),
            placeholder_text=template.placeholder_text,
            post_doc_commands=template.post_doc_commands,
        )

        formula = MathTex(r"\text{если }",
                            r"d_{ij}",
                            r">",
                            r"d_{ik}",
                            r"+",
                            r"d_{kj}",
                            r"\text{, то }",
                            r"d_{ij}",
                            r":=",
                            r"d_{ik}",
                            r"+",
                            r"d_{kj}",
                            tex_template=new_template).scale(0.7)
        formula.to_edge(UP)
        formula_if = formula[:6]
        formula_then = formula[6:]
        formula[1].set_color(GREEN)
        formula[3].set_color(BLUE)
        formula[5].set_color(RED)
        formula[7].set_color(GREEN)
        formula[9].set_color(BLUE)
        formula[11].set_color(RED)


        # Draw a copy of the formula below the first one
        copy_formula = formula.copy()
        copy_formula[0].fade(1)
        copy_formula[6].fade(1)
        

        self.play(Write(formula))
        self.add(copy_formula)
        self.play(copy_formula.animate.next_to(copy_formula, DOWN))
        self.remove(copy_formula)
        for item in copy_formula:
            self.add(item)
        self.wait()


        def make_dijk(i, j, k):
            dij = MathTex(r"d_{" + f'{i}' + f'{j}' + r"}").scale(0.7).set_color(GREEN)
            dik = MathTex(r"d_{" + f'{i}' + f'{k}' + r"}").scale(0.7).set_color(BLUE)
            dkj = MathTex(r"d_{" + f'{k}' + f'{j}' + r"}").scale(0.7).set_color(RED)
            return dij, dik, dkj

        for k in range(len(graph)):

            self.add(copy_formula[1], copy_formula[3], copy_formula[5])
            vk = str(k + 1)
            col_rect = SurroundingRectangle(mat.get_columns()[k], buff=0.1).fade(0.5)
            row_rect = SurroundingRectangle(mat.get_rows()[k], buff=0.1).fade(0.5)
            self.play(Create(col_rect), Create(row_rect))



            dij, dik, dkj = make_dijk('i', 'j', vk)
            dik_if = dik.copy().move_to(formula[3])
            dkj_if = dkj.copy().move_to(formula[5])
            dij_then = dij.copy().move_to(formula[7])
            dkj_then = dkj.copy().move_to(formula[9])

            self.play(
                formula[3].animate.become(dik_if),
                formula[5].animate.become(dkj_if),
                formula[7].animate.become(dij_then),
                formula[9].animate.become(dkj_then),
                FocusOn(formula[3]))

            self.wait()

            def dedup(mobject):
                to_remove = []
                for m in self.mobjects:
                    if (m.get_center() == mobject.get_center()).all():
                        to_remove.append(m)
                for item in to_remove:
                    if item is not mobject:
                        self.remove(item)
                print("Removed:", to_remove)
    
            # Graph needs to be realigned because the matrix's elements have shifted
            #new_mat = Matrix(graph)
            #self.play(Transform(mat, new_mat))
            #self.remove(new_mat)
            #mat = new_mat


            AAA = 0
            RT = 0.5

            current_cell_box = None
            for i in range(len(graph)):
                for j in range(len(graph)):

                    if i==k or j==k: continue
                    #if AAA == 2: continue

                    AAA += 1

                    dij, dik, dkj = make_dijk(i+1, j+1, vk)
                    dij_if = dij.copy().move_to(formula[1])
                    dij_then = dij.copy().move_to(formula[7])
                    dik_if = dik.copy().move_to(formula[3])
                    dik_then = dik.copy().move_to(formula[9])
                    dkj_if = dkj.copy().move_to(formula[5])
                    dkj_then = dkj.copy().move_to(formula[11])

                    idij, idik, idkj = make_dijk('i', 'j', 'k')
                    idij_if = idij.copy().move_to(copy_formula[1])
                    idik_if = idik.copy().move_to(copy_formula[3])
                    idkj_if = idkj.copy().move_to(copy_formula[5])
                    idij_then = idij.copy().move_to(copy_formula[7])
                    idik_then = idik.copy().move_to(copy_formula[9])
                    idkj_then = idkj.copy().move_to(copy_formula[11])
                    self.play(
                        formula[1].animate.become(dij_if),
                        formula[3].animate.become(dik_if),
                        formula[5].animate.become(dkj_if),
                        formula[7].animate.become(dij_then),
                        formula[9].animate.become(dik_then),
                        formula[11].animate.become(dkj_then),

                        copy_formula[1].animate.become(idij_if),
                        copy_formula[3].animate.become(idik_if),
                        copy_formula[5].animate.become(idkj_if),
                        copy_formula[7].animate.become(idij_then),
                        copy_formula[9].animate.become(idik_then),
                        copy_formula[11].animate.become(idkj_then),
                        run_time=RT
                    )


                    new_cell_box = SurroundingRectangle(mat.get_rows()[i][j], buff=0.1, color=GREEN).fade(0.5)
                    if current_cell_box is not None:
                        self.play(Transform(current_cell_box, new_cell_box), formula[1].animate.become(dij_if), formula[7].animate.become(dij_then), run_time=RT)
                    else:
                        self.play(Create(new_cell_box), formula[1].animate.become(dij_if), formula[7].animate.become(dij_then), run_time=RT)
                        current_cell_box = new_cell_box
                    
                    hor_cell_box = SurroundingRectangle(mat.get_rows()[i][k], buff=0.1, color=BLUE).fade(0.5)
                    ver_cell_box = SurroundingRectangle(mat.get_rows()[k][j], buff=0.1, color=RED).fade(0.5)

                    current_into_hor = current_cell_box.copy()
                    current_into_ver = current_cell_box.copy()
                    self.play(Transform(current_into_hor, hor_cell_box), Transform(current_into_ver, ver_cell_box), run_time=RT)
                    #self.remove(current_into_hor, current_into_ver)

                    formula_if_underline = Underline(formula_if, buff=0.1).set_color(YELLOW).reverse_direction()
                    formula_then_underline = Underline(formula_then, buff=0.1).set_color(YELLOW)
                    self.play(Create(formula_if_underline), run_time=RT)
                    current_cell = mat.get_rows()[i][j]
                    current_cell_copy = current_cell.copy()
                    #self.add(current_cell_copy)
                    current_cell_copy_in_place = current_cell_copy.copy().move_to(copy_formula[1]).set_color(GREEN)
                    
                    hor_cell = mat.get_rows()[i][k]
                    hor_cell_copy = hor_cell.copy()
                    #self.add(hor_cell_copy)
                    hor_cell_copy_in_place = hor_cell_copy.copy().move_to(copy_formula[3]).set_color(BLUE)

                    vert_cell = mat.get_rows()[k][j]
                    vert_cell_copy = vert_cell.copy()
                    #self.add(vert_cell_copy)
                    vert_cell_copy_in_place = vert_cell_copy.copy().move_to(copy_formula[5]).set_color(RED)

                    self.play(
                        FadeOut(copy_formula[1]),
                        ClockwiseTransform(current_cell_copy, current_cell_copy_in_place),
                        FadeOut(copy_formula[3]),
                        ClockwiseTransform(hor_cell_copy, hor_cell_copy_in_place),
                        FadeOut(copy_formula[5]),
                        ClockwiseTransform(vert_cell_copy, vert_cell_copy_in_place), run_time=RT
                    )
                    copy_formula[1].become(current_cell_copy_in_place)
                    copy_formula[3].become(hor_cell_copy_in_place)
                    copy_formula[5].become(vert_cell_copy_in_place)

                    self.remove(#current_cell_copy, hor_cell_copy, vert_cell_copy,
                                current_cell_copy_in_place, hor_cell_copy_in_place, vert_cell_copy_in_place)

                    self.wait(RT)
                    
                    cur_value = graph[i][j] if graph[i][j] != X else float('inf')
                    hor_value = graph[i][k] if graph[i][k] != X else float('inf')
                    vert_value = graph[k][j] if graph[k][j] != X else float('inf')
                    if cur_value > hor_value + vert_value:
                        current_cell_copy_in_then = current_cell_copy_in_place.copy().move_to(copy_formula[7])
                        hor_cell_copy_in_then = hor_cell_copy_in_place.copy().move_to(copy_formula[9])
                        vert_cell_copy_in_then = vert_cell_copy_in_place.copy().move_to(copy_formula[11])
                        current_cell_copy_in_place_from = current_cell_copy_in_place.copy()
                        hor_cell_copy_in_place_from = hor_cell_copy_in_place.copy()
                        vert_cell_copy_in_place_from = hor_cell_copy_in_place.copy()
                        self.play(
                            ClockwiseTransform(current_cell_copy_in_place_from, current_cell_copy_in_then),
                            FadeOut(copy_formula[7]),
                            ClockwiseTransform(hor_cell_copy_in_place_from, hor_cell_copy_in_then),
                            FadeOut(copy_formula[9]),
                            ClockwiseTransform(vert_cell_copy_in_place_from, vert_cell_copy_in_then),
                            FadeOut(copy_formula[11]),
                            run_time=RT)
                        self.remove(current_cell_copy_in_place_from, hor_cell_copy_in_place_from, vert_cell_copy_in_place_from)
                        copy_formula[7].become(current_cell_copy_in_then)
                        copy_formula[9].become(hor_cell_copy_in_then)
                        copy_formula[11].become(vert_cell_copy_in_then)
                        self.add(copy_formula[7], copy_formula[9], copy_formula[11])
                        self.remove(current_cell_copy_in_then, )# hor_cell_copy_in_then, vert_cell_copy_in_then)
                        self.play(Uncreate(formula_if_underline), Create(formula_then_underline), run_time=RT)

                        new_value = hor_value + vert_value
                        old_cells = VGroup(copy_formula[7], copy_formula[9], copy_formula[11])
                        #self.play(LaggedStartMap(FocusOn, [hor_cell_copy_in_then, vert_cell_copy_in_then, current_cell_copy_in_then], ))
                        #self.wait(RT)
                        #self.play(LaggedStartMap(Wiggle, [copy_formula[7], copy_formula[9], copy_formula[11]], scale_value=1.5))
                        #dedup(copy_formula[7])
                        new_cell = MathTex(str(new_value)).set_color(GREEN).move_to(copy_formula[7])

                        hor_cell_final_copy = copy_formula[9].copy()
                        vert_cell_final_copy = copy_formula[11].copy()
                        self.add(hor_cell_final_copy, vert_cell_final_copy)

                        self.play(
                            Transform(old_cells, new_cell, remover=False), run_time=RT
                        )

                        self.remove(old_cells)
                        self.remove(hor_cell_copy_in_then, vert_cell_copy_in_then, current_cell_copy_in_then)
                        #self.add(new_cell)

                        copy_formula[7].become(new_cell)
                        copy_formula[9].become(hor_cell_final_copy)
                        copy_formula[11].become(vert_cell_final_copy)
                        self.remove(hor_cell_final_copy, vert_cell_final_copy)
                        self.add(copy_formula[7], copy_formula[9], copy_formula[11])


                        new_cell_in_place = new_cell.copy().move_to(mat.get_rows()[i][j]).set_color(WHITE)
                        self.play(
                            FadeOut(mat.get_rows()[i][j]),
                            ClockwiseTransform(new_cell.copy(), new_cell_in_place),
                            Uncreate(formula_then_underline), run_time=RT
                        )
                        mat.get_rows()[i][j].become(new_cell_in_place)
                        graph[i][j] = new_value
                        

                    else:
                        if_formulas = VGroup(formula[:6],copy_formula[:6])
                        if_formulas_cross = Cross(if_formulas)
                        self.play(Create(if_formulas_cross), run_time=RT)
                        self.play(
                            FadeOut(if_formulas_cross),
                            Uncreate(formula_if_underline), run_time=RT
                        )
                    
                    self.remove(current_into_hor, current_into_ver)

                    self.play(FadeOut(hor_cell_box), FadeOut(ver_cell_box))
                    self.remove(current_cell_copy, hor_cell_copy, vert_cell_copy,)

            self.add(copy_formula[1], copy_formula[3], copy_formula[5])
            self.play(FadeOut(col_rect), FadeOut(row_rect), FadeOut(current_cell_box))

        self.wait(2)
        return  # Code below this doesn't work yet.
        self.play(FadeOut(mat), FadeOut(copy_formula), FadeOut(formula), FadeOut(formula_then_underline), FadeOut(formula_if_underline))
        self.play(Create(initial_graph))
        self.play(initial_graph.animate.shift(2*LEFT).scale(0.5))
        final_edges = []
        final_edges_conf = dict()
        min_weight = float('inf')
        max_weight = 0
        for i in range(len(graph)):
            for j in range(len(graph[i])):
                if graph[i][j] != X:
                    min_weight = min(min_weight, graph[i][j])
                    max_weight = max(max_weight, graph[i][j])

        grad = color_gradient([PURE_RED, PURE_GREEN], max_weight - min_weight + 1)
        for i in range(len(graph)):
            for j in range(len(graph)):
                if graph[j][i] != X:
                    final_edges.append( (f"V_{j+1}", f"V_{i+1}") )
                    final_edges_conf[(f"V_{j+1}", f"V_{i+1}")] = {
                        "stroke_color": grad[ graph[j][i] - min_weight ],
                    }

        final_graph = Graph(VERT_NAMES, final_edges, edge_config=final_edges_conf, layout='circular', edge_type=Arrow)
        final_graph.shift(2*RIGHT).scale(0.5)
        
        self.play(
            Create(final_graph),
        )
        self.wait(5)
        self.play(FadeOut(initial_graph), FadeOut(final_graph))
