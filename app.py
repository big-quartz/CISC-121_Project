import random
import gradio as gr

# Generate random list
def random_list(n):
    #List comprehension that creates and returns a random list of integers between 1 and 100
    return [random.randint(1, 100) for _ in range(n)]

# Selection sort that records steps
def selection_sort(unsorted):
    LENGTH = len(unsorted) #Length of the list of integers
    i = 0 #pointer that shows where the smallest number must be
    steps = []#list to store each step


    #outer loop that divides the sorted and unsorted
    while i < LENGTH - 1:
        min_index = i
        j = i + 1 #pointer that scans the unsorted part of the list

        #inner loop that campares with j to make sure smallest is at j
        while j < LENGTH:
            #record before comparision
            steps.append({"array": unsorted.copy(), "i": i, "j": j, "min_index": min_index})

            #update min index if smaller value is found
            if unsorted[j] < unsorted[min_index]:
                min_index = j 
                steps.append({"array": unsorted.copy(), "i": i, "j": j, "min_index": min_index})
            j += 1

        #after iterating through the unsorted part swap if min index is not at i
        if min_index != i:
            unsorted[i], unsorted[min_index] = unsorted[min_index], unsorted[i]
            #record state after swap
            steps.append({"array": unsorted.copy(), "i": i, "j": j, "min_index": min_index})
        i += 1
    #return list of states
    return steps

# Render step as HTML
def render_step(step):
    #extract the data from step dictionary
    arr = step["array"]
    i = step["i"]
    j = step["j"]
    m = step["min_index"]

    #start an HTML container that lays out the elments horizontally
    html = "<div style='display:flex;gap:16px;justify-content:center;'>"

    #loop through each value in the array, while higlighting the pointers and min
    for idx, val in enumerate(arr):
        color = "#f0f0f0"
        label = ""
        if idx == m:
            color = "#90ee90"
            label = "min"
        if idx == i:
            color = "#87cefa"
            label = "i"
        if idx == j:
            color = "#ffcccb"
            label = "j"
        #add a box for each array element
        html += f"""
            <div style="text-align:center">
                <div style="
                    background:{color};
                    padding:10px 14px;
                    border-radius:6px;
                    font-weight:bold;
                    min-width:30px;
                    color:black;
                ">
                    {val}
                </div>
                <small>{label}</small>
            </div>"""
    html += "</div>"
    #return the HTML string
    return html

# Generate new list & steps
def generate(n):
    rand_list = random_list(n)
    steps = selection_sort(rand_list)
    return steps, 0, render_step(steps[0]), f"Step 1 / {len(steps)}"

# Go to next step when next button is clicked
def next_step(steps, idx, active):
    #if already at last step, stay there
    if idx >= len(steps) - 1:
        return idx, render_step(steps[-1]), f"Step {len(steps)} / {len(steps)}"
    #if else move a step and return updated index and visual
    idx += 1
    return idx, render_step(steps[idx]), f"Step {idx + 1} / {len(steps)}"

#automatically advance steps steps if auto play is active
def auto_next(steps, idx, active):
    #if auto play is turned off, do nothing
    if not active:
        return gr.NO_UPDATE, gr.NO_UPDATE, gr.NO_UPDATE, gr.NO_UPDATE

    #if at last step stop auto play
    if idx >= len(steps) - 1:
        return idx, render_step(steps[-1]), f"Step {len(steps)} / {len(steps)}", False

    #else go to next step
    idx += 1
    return idx, render_step(steps[idx]), f"Step {idx+1} / {len(steps)}", active

#NOTE: i could not understand how to make gradio ticker only tick while the auto play is on, 
#therefore the visualizer updates every .5s regardless of whether auto play is on or not


# Gradio UI

#create container
with gr.Blocks(title="Selection Sort Visualizer") as demo:
    #app title at top
    gr.Markdown("# 📊 Selection Sort — Step by Step Visualizer")

    #state variables that persist betwen interactions
    steps_state = gr.State()
    step_index = gr.State(0)
    auto_active = gr.State(False)

    #UI components that update dynamically
    step_counter = gr.Markdown()
    array_md = gr.HTML()  

    size_slider = gr.Slider(minimum=5, maximum=15, value=10, step=1, label="List size")

    with gr.Row():
        gen_btn = gr.Button("Generate List")
        next_btn = gr.Button("Next ➡")
        auto_btn = gr.Button("Auto Play ▶")
        stop_btn = gr.Button("Stop ⏹")

    auto_timer = gr.Timer(0.5, False)
    
    gen_btn.click(generate, inputs=[size_slider], outputs=[steps_state, step_index, array_md, step_counter])
    next_btn.click(next_step, inputs=[steps_state, step_index], outputs=[step_index, array_md, step_counter])
    auto_btn.click(lambda: True, [], auto_active)
    auto_timer.tick(auto_next, inputs=[steps_state, step_index, auto_active], outputs=[step_index, array_md, step_counter, auto_active])
    stop_btn.click(lambda: False, [], auto_active)

demo.launch()
