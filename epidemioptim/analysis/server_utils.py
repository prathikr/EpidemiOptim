#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 12:02:27 2020

@author: ddutartr
"""
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../../')

from epidemioptim.utils import *
from epidemioptim.analysis.notebook_utils import setup_for_replay,replot_stats,setup_fig_notebook,run_env,get_action_base
from ipywidgets import HTML,Layout,VBox,FloatSlider,IntSlider,HBox,Label,ToggleButton,Dropdown,Checkbox,interactive_output,Box, Text, Output, Button
from IPython.display import display
import time
# About


# -apple-system,.SFNSText-Regular,San Francisco,Segoe UI,Helvetica Neue,Lucida Grande,
p_style = 'style="line-height:150%;font-weight:300;font-size:22px;font-family:Hind,sans-serif;"'
h3_style = 'style="color:#004c8f;line-height:150%;font-weight:700;font-size:24px;font-family:Montserrat,sans-serif;">'
h2_style = 'style="color:#004c8f;line-height:150%;font-weight:700;font-size:40px;font-family:Montserrat,sans-serif;">'
h2_style_2 = 'style="color:#004c8f;line-height:150%;font-weight:700;font-size:35px;font-family:Montserrat,sans-serif;">'
def introduction():

    intro_html=HTML(layout=Layout(width='800px',
                                  height='100%',
                                  margin='auto',
                                  ),
                    value=(' <link href="https://fonts.googleapis.com/css2?family=Hind:wght@300;400;500;600;700&family=Montserrat:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;1,100;1,200;1,300;1,400;1,500;1,600;1,700&display=swap" rel="stylesheet"> ' +
                            "<font color='black'><font face = 'Comic sans MS'>" +
                           '<center><h2 ' + h2_style + 'Using AI to Design Intervention Strategies Against Epidemics</h2></center>'
                           +'<p>&nbsp;</p>'
                           + '<center><figure> <img src="logo_inserm_inria.png" width="500px"></figure></center>'
                           + '<p>&nbsp;</p>'
                           + '<center><figure> <img src="visu.gif" alt="COVID-19 epidemic in France" /> <figcaption ' + p_style +'>'
                           'Evolution of French COVID-19 cases in intensive care<br>from March to November 2020.</figcaption></figure></center>'
                           + '<p>&nbsp;</p>'
                           +'<h3 ' + h3_style + 'Context</h3>'
                           +'<p align="justify" ' + p_style + '>'
                           +'Epidemiologists  model  the  dynamics  of  epidemics  in  order  to  propose  mitigation strategies based on pharmaceutical and non-pharmaceutical '
                            'interventions (contact limitation,  lock down,  vaccination,  etc.). '
                           +'Hand-designing such strategies is not trivial because of the number of possible interventions and the difficulty to predict their long-term effects.  '
                            'This task can be seen as an optimization problem where state-of-the-art  machine  learning  algorithms  might  '
                            'bring  significant value. </p>'
                           +'<p align="justify" ' + p_style + '>'
                           + 'This website presents an interactive demo of a set of machine learning methods we presented in our research paper: '
                           + '<a href="https://arxiv.org/pdf/2010.04452.pdf" style="color:#004c8f;" target="_blank">EpidemiOptim: A Toolbox for the Optimization of Control '
                             'Policies in Epidemiological Models</a>. The full code of this toolbox is open-source and available on github '
                           + '<a href="https://github.com/flowersteam/EpidemiOptim"> here </a>.'
                           + '</p>'
                           + '<p>&nbsp;</p>'
                           +'<h3 ' + h3_style + 'Interact with trained models, design your own intervention strategy!</h3>'
                           +'<p align="justify" ' + p_style + '>'
                           +'To demonstrate the use of EpidemiOptim, we run experiments to optimize the design of an on/off lock-down policy in the context of the COVID-19 '
                            'epidemic in the French region of Ile-de-France. </p>'
                           + '<p align="justify" ' + p_style + '>'
                           +'We have two objectives here: minimizing the death toll and minimizing the economic recess. '
                           +'In the tabs below, you will be able to <span style="font-weight:500;">explore strategies optimized by various optimization algorithms</span>. '
                           +'In the last tab, you will be able to <span style="font-weight:500;">design your own strategy</span>, apply it over a year of epidemic and observe its health and economic consequences.'
                           +'</p><p>&nbsp;</p><p>&nbsp;</p> '

                           +'</font>'))
    return intro_html

def footer():
    footer = HTML(layout=Layout(width='800px',
                                    height='100%',
                                    margin='auto',
                                    ),
                      value=(
                                  '<link href="https://fonts.googleapis.com/css2?family=Hind:wght@300;400;500;600;700&family=Montserrat:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;1,100;1,200;1,300;1,400;1,500;1,600;1,700&display=swap" rel="stylesheet"> ' +
                                  "<font color='black'><font face = 'Comic sans MS'>"
                                  + '<p>&nbsp;</p><p>&nbsp;</p>'
                                  + '<h3 ' + h3_style + 'Acknowledgements</h3>'
                                  + '<p align="justify" ' + p_style + '>'
                                  + 'This work is supported inpart by Inria Mission COVID19, project GESTEPID. '
                                  + 'It is the product of a collaboration between the <a '
                                    'href="https://www.bordeaux-population-health.center/les-equipes/statistiques-pour-la-medecine-translationnelle-sistm/"'
                                    'style="color:#004c8f;" target="_blank">Inria SISTM team</a> (epidemiology) and the <a href="https://flowers.inria.fr/"'
                                    'style="color:#004c8f;" target="_blank">Inria Flowers team</a> (optimization). We would like to thank Sebastien Rouillon (Univ. de Bordeaux) '
                                    'for his contribution on the elaboration of the model of economic recess and Dan Dutartre (Inria) for the design of this web interface. '
                                    'The paper describing the approach can be found <a href="https://arxiv.org/pdf/2010.04452.pdf" style="color:#004c8f;" '
                                    'target="_blank">here</a>.</p>'

                                  + '<h3 ' + h3_style + 'Reference</h3>'
                                  + '<p align="left" ' + p_style + '>'
                                  + 'The bibtex reference to the EpidemiOptim paper can be found here:'
                                  + '<p>&nbsp;</p>'
                                  + '<code> @article{colas2020epidemioptim, <br>'
                                  + '&nbsp;&nbsp;&nbsp;&nbsp;title={EpidemiOptim: A Toolbox for the Optimization of Control Policies in Epidemiological<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Models}, <br>'
                                  + '&nbsp;&nbsp;&nbsp;&nbsp;author={Colas, C{\'e}dric and Hejblum, Boris and Rouillon, S{\'e}bastien and Thi{\'e}baut, '
                                    '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Rodolphe and Oudeyer, '
                                    ' Pierre-Yves and Moulin-Frier, Cl{\'e}ment and Prague, M{\'e}lanie}, <br>'
                                  + '&nbsp;&nbsp;&nbsp;&nbsp;journal={arXiv preprint arXiv:2010.04452}, <br>'
                                  + '&nbsp;&nbsp;&nbsp;&nbsp;year={2020}} </code>'
                                  + '</p><p>&nbsp;</p><p>&nbsp;</p>'
                                  + '</font>'))
    return footer

def algorithm_description(algorithm):
    if algorithm=='DQN':
        str_html=HTML(layout=Layout(width='800px',
                                  height='100%',
                                  margin='auto',
                                  ),
                    value=("<font color='black'><font face = 'Verdana'>" +
                           '<center><h2 ' + h2_style_2 + 'Algo 1: Deep Q-Networks (DQN)</h2></center>'
                           + '<p>&nbsp;</p>'
                           +'<h3 ' + h3_style + 'Objective</h3>'
                           +'<p align="justify" ' + p_style + '>'
                           +'We want to minimize two costs: the death toll <var>C<sub>health</sub></var> and the economic recess <var>C<sub>economic</sub></var> computed over a one-year period.'
                           + '</p>'
                           + '<h3 ' + h3_style + 'The algorithm</h3>'
                           +'<p align="justify" ' + p_style + '>'
                           + 'The first algorithm belongs to the family of <span style="font-weight:500;">reinforcement learning</span> algorithms: <span style="font-weight:500;">Deep Q-Networks ('
                           + 'DQN)</span>. DQN is traditionally used to minimize a unique cost function. To circumvent this problem, we train several control policies, '
                           + 'where each policy minimizes a certain combination of the two costs:</p>'
                           + '<p align="center" ' + p_style + '>'
                           +'<var>C</var> = (1 - &#946) &#215 <var>C<sub>h</sub></var> +  &#946 &#215 <var>C<sub>e</sub></var> ,'
                           + '</p>'
                           + '<p align="justify" ' + p_style + '>'
                           +'where <var>C</var> is the aggregated cost and &#946 is the mixing parameter. The lower the &#946 the more important the health cost.</p>'
                           +'<h3 ' + h3_style + 'What is plotted</h3>'
                           +'<p align="justify" ' + p_style + '>'
                           +'The four plots below show the evolution of the daily economic and health costs over a one-year period (left: per day; right: cumulated). Red dots '
                            'indicate lock-down enforcement for the corresponding week. '
                           +'<h3 ' + h3_style + 'Try it yourself!</h3>'
                           +'<p align="justify" ' + p_style + '>'
                           +'The slider &#946 allows to control the mixing of the two costs. &#946 = 1 results in the pure minimization of the economic cost. '
                            '&#946 = 0 results in the pure minimization of the death toll. The <span style="font-weight:500;">deterministic model</span> box controls whether the epidemic '
                            'is deterministic (always the same), or stochastic (always different).'
                           + '</p>'
                           +'</font>'))
    elif algorithm=='GOAL_DQN':
        str_html=HTML(layout=Layout(width='800px',
                                  height='100%',
                                  margin='auto',
                                  ),
                    value=("<font color='black'><font size = 5><font face = 'Verdana'>" +
                           '<center><h2 ' + h2_style_2 + 'Algo 2: Goal-Conditioned Deep Q-Networks (Goal-DQN)</h2></center>'
                           + '<p>&nbsp;</p>'
                           +'<h3 ' + h3_style + 'Objective</h3>'
                           +'<p align="justify" ' + p_style + '>'
                           +'We want to minimize two costs: the death toll <var>C<sub>health</sub></var> and the economic recess <var>C<sub>economic</sub></var> computed over a one-year period.'
                           + '</p>'
                           + '<h3 ' + h3_style + 'The algorithm</h3>'
                           +'<p align="justify" ' + p_style + '>'
                           +'This algorithm is a variant of the traditional <span style="font-weight:500;">Deep Q-Network</span>. In the <span style="font-weight:500;">Goal-Conditioned Q-Networks (Goal-DQN)</span>, we train one policy to minmize all the combinations of the health and economic costs:'
                           + '<p align="center" ' + p_style + '>'
                           +'<var>C</var> = (1 - &#946) &#215 <var>C<sub>h</sub></var> +  &#946 &#215 <var>C<sub>e</sub></var> ,'
                           + '</p>'
                           + '<p align="justify" ' + p_style + '>'
                           +'for all values of &#946 in [0, 1].</p>'
                           + '<p align="justify" ' + p_style + '>'
                           +'To do so, the policy receives the value of &#946 corresponding to the mixture of costs it needs to minimize. This dramatically reduces '
                            'training time compared to a simple DQN (Algo 1 tab), as only one policy is trained.'
                           + '</p>'
                           +'<h3 ' + h3_style + 'What is plotted</h3>'
                           +'<p align="justify" ' + p_style + '>'
                           +'The four plots below show the evolution of the daily economic and health costs over a one-year period (left: per day; right: cumulated). Red dots '
                            'indicate lock-down enforcement for the corresponding week. '
                           +'<h3 ' + h3_style + 'Try it yourself!</h3>'
                           +'<p align="justify" ' + p_style + '>'
                           +'The slider &#946 allows to control the mixing of the two costs. &#946 = 1 results in the pure minimization of the economic cost. &#946 = 0 '
                            'results in the pure minimization of the death toll. The <span style="font-weight:500;">deterministic model</span> box controls whether the epidemic '
                            'is deterministic (always the same), or stochastic (always different). '
                           + '</p>'
                           +'</font>'))
    elif algorithm=='GOAL_DQN_CONST':
        str_html=HTML(layout=Layout(width='800px',
                                  height='100%',
                                  margin='auto',
                                  ),
                    value=("<font color='black'><font size = 5><font face = 'Verdana'>" +
                           '<center><h2 ' + h2_style_2 + 'Algo 3: Goal-Conditioned Deep Q-Networks with Constraints (Goal-DQN-C)</h2></center>'
                           + '<p>&nbsp;</p>'
                           +'<h3 ' + h3_style + 'Objective</h3>'
                           +'<p align="justify" ' + p_style + '>'
                           +'We want to minimize two costs: the death toll <var>C<sub>health</sub></var> and the economic recess <var>C<sub>economic</sub></var> computed over a one-year period.'
                           + '</p>'
                           + '<h3 ' + h3_style + 'The algorithm</h3>'
                           +'<p align="justify" ' + p_style + '>'
                           +'This algorithm is a variant of the traditional <span style="font-weight:500;">Deep Q-Network</span>. In the <span style="font-weight:500;">Goal-Conditioned Q-Networks with Constraints (Goal-DQN-C)</span>, we train one policy to minmize all the combinations of the health and economic costs:'
                           + '<p align="center" ' + p_style + '>'
                           +'<var>C</var> = (1 - &#946) &#215 <var>C<sub>h</sub></var> +  &#946 &#215 <var>C<sub>e</sub></var> ,'
                           + '</p>'
                           + '<p align="justify" ' + p_style + '>'
                           +'for all values of &#946 in [0, 1].</p>'
                           + '<p align="justify" ' + p_style + '>'
                           +' In addition, we can set constraints on maximum values for each of the cumulated cost over the one-year period. To do so, the policy receives the value of &#946 corresponding to the mixture of costs it needs to minimize, as well as the value of the maximum cumulative cost that forms its constraints .'
                           + '</p>'
                           +'<h3 ' + h3_style + 'What is plotted</h3>'
                           +'<p align="justify" ' + p_style + '>'
                           +'The four plots below show the evolution of the daily economic and health costs over a one-year period (left: per day; right: cumulated). Red dots '
                            'indicate lock-down enforcement for the corresponding week. '
                           +'<h3 ' + h3_style + 'Try it yourself!</h3>'
                           +'<p align="justify" ' + p_style + '>'
                           +'The slider &#946 allows to control the mixing of the two costs. &#946 = 1 results in the pure minimization of the economic cost. &#946 = 0 '
                            'results in the pure minimization of the death toll. The <span style="font-weight:500;">deterministic model</span> box controls whether the epidemic '
                            'is deterministic (always the same), or stochastic (always different).'
                           +' The other two sliders control the maximum values the cumulative costs can take. Explore the effect of these parameters. Note how the policy adapts to the constraints. If you push further, and set strong constraints on the two costs, a good policy might not exist (e.g. 0 death and 0 euros of economic recess.)'
                           + '</p>'
                           +'</font>'))
    elif algorithm=='NSGA':
        str_html=HTML(layout=Layout(width='800px',
                                  height='100%',
                                  margin='auto',
                                  ),
                    value=("<font color='black'><font size = 5><font face = 'Verdana'>" +
                           '<center><h2 ' + h2_style_2 + 'Algo 4: Non-dominated Sorting Genetic Algorithm II (NSGA-II)</h2></center>'
                           + '<p>&nbsp;</p>'
                           +'<h3 ' + h3_style + 'Objective</h3>'
                           +'<p align="justify" ' + p_style + '>'
                           +'We want to minimize two costs: the death toll <var>C<sub>health</sub></var> and the economic recess <var>C<sub>economic</sub></var> computed over a one-year period.'
                           + '</p>'
                           + '<h3 ' + h3_style + 'The algorithm</h3>'
                           +'<p align="justify" ' + p_style + '>'
                           +'<span style="font-weight:500;">Non-dominated Sorting Genetic Algorithm II (NSGA-II)</span> is a state-of-the-art multi-objective optimization algorithm from the family of evolutionary algorithms. In contrast to previous algorithms, this one is explicitely built to optimize several costs at a time instead of linear combinations of them. In practice, this algorithm aims to find a '
                           +'<span style="font-weight:500;">Pareto Front</span>, the set of <span style="font-weight:500;">non-dominated solutions</span>: solutions for which one cannot find any other solution that performs better on both dimensions (better health cost <span style="font-weight:500;">and</span> better economic cost). The result of this algorithm is thus a set of control policies, each having their particular trade-off with respect to the two costs.'
                           +'<h3 ' + h3_style + 'What is plotted</h3>'
                           +'<p align="justify" ' + p_style + '>'
                           +'The first plot represents the Pareto front found by one run of the NSGA-II algorithm. Note that no solution performs better than any other on both dimensions, or worse on both dimensions. Each point represent the average performance of a given policy on the two costs, after it is run on 30 different simulations of the epidemic. The four plots below show the evolution of the daily economic and health costs over a one-year period. Red dots indicate lock-down enforcement for the corresponding week. '
                           +'<h3 ' + h3_style + 'Try it yourself!</h3>'
                           +'<p align="justify" ' + p_style + '>'
                           +'You can click on points in the first plot to select the corresponding policy and see its consequences in terms of the two costs in the graphs below. '
                            'When the <span style="font-weight:500;">deterministic model</span> box is unchecked, the model becomes stochastic:  '
                            'each time you click on the policy a new simulation is run, and the way the policy reacts to the epidemic might vary.'
                           + '</p>'
                           +'</font>'))
    elif algorithm=='yourself':
        str_html=HTML(layout=Layout(width='800px',
                                  height='100%',
                                  margin='auto',
                                  ),
                          value=("<font color='black'><font face = 'Verdana'>" +
                                 '<center><h2 ' + h2_style_2 + 'Try It Yourself!</h2></center>'
                                 + '<p>&nbsp;</p>'
                                 +'<h3 ' + h3_style + 'Objective</h3>'
                                 +'<p align="justify" ' + p_style + '>'
                                 +'We want to minimize two costs: the death toll <var>C<sub>health</sub></var> and the economic recess <var>C<sub>economic</sub></var> computed over a one-year period.'
                                 + '</p>'
                                 + '<h3 ' + h3_style + 'The algorithm</h3>'
                                 +'<p align="justify" ' + p_style + '>'
                                 + 'Here, you are the algorithm!'
                                 +'<h3 ' + h3_style + 'What is plotted</h3>'
                                 +'<p align="justify" ' + p_style + '>'
                                 +'The first plot represents the Pareto front found by one run of the NSGA-II algorithm. The red dot is the average performance of the strategy you design (computed over 30 simulations). The four plots below show the evolution of the daily economic and health costs over a one-year period. Red dots indicate lock-down enforcement for the corresponding week. '
                                 +'<h3 ' + h3_style + 'Try it yourself!</h3>'
                                 +'<p align="justify" ' + p_style + '>'
                                 +'To perform better than NSGA-II, you need to get closer to the origin of the plot (0, 0). Note that algorithms train policies that are '
                                  'reactive to the epidemic and can adapt to its state as it progresses. You are designing, on the other hand, '
                                  'a <span style="font-weight:500;">fixed-strategy</span> that is evaluated on 10 different simulated epidemics. This explains why running '
                                  'several evaluations might result in different results. The graphs shows only one of the 10 simulations.'
                                 + '<br>You can design your strategy with two tools:'
                                 + '<ol ' + p_style +'><li>The four dropdown menus allow to define a pattern of the form: '
                                 + '<span style="font-weight:500;"> implement lock-down N1 weeks every N2 weeks</span>.'
                                 + ' The first two menus control the start and end of the pattern (in weeks), the following two respectively '
                                 + 'control the duration of the lock-down and the period of the pattern. Click <span style="font-weight:500;">"Set to pattern"</span> '
                                   'to synchronize the checkboxes and implement the intervention. </li>'
                                 +'<li>The checkboxes control the enforcement of the lockdown on a weekly basis. You can finetune the intervention defined by the '
                                  'pattern by checking/unchecking specific boxes. Once you are ready, run the simulations by clicking <span style="font-weight:500;">"Run '
                                  'simulations"</span>.</li></ol>'
                                 + '</p>'
                                 +'</font>'))
            
    else:
        NotImplementedError
    
    return str_html

def slider_setup(slider):
    slider.layout.max_width = '100%'
    #desc=slider.description
    #slider.description=''
    #sliderHbox=HBox([Label(desc,style={'description_width' : 'initial'}),slider])
    return slider
def modify_description(slider):
    desc=slider.description
    slider.description=''
    sliderHbox=HBox([Label(desc,style={'description_width' : 'initial'}),slider])
    return sliderHbox
def update_fig(fig):
    fig.canvas.draw_idle()
    fig.canvas.draw()
    fig.canvas.flush_events()
    return fig
def canvas_setup(fig):
    fig.canvas.header_visible = False
    fig.canvas.toolbar_visible = False
    fig.canvas.layout.min_height = '400px'
    return fig

def deter_checkbox():
    is_deter=Checkbox(
        value=True,
        description='Deterministic model',
        disabled=False,
        indent=False,
        layout={'max_width': '100%'})
    return is_deter

def plot_pareto(algorithm,size,color):
    # Plot pareto front
    fig = plt.figure()
    ax = fig.add_subplot(111)
    sign = 1
    a = sign * algorithm.res_eval['F'][:, 0]
    b = sign * algorithm.res_eval['F'][:, 1]
    nb_points=a.shape[0]
    sc = ax.scatter(a, b, picker=5)
    ax.tick_params(axis='x', labelrotation=30,labelsize=12)
    ax.tick_params(axis='y',labelsize=12)
    colors = [color] * nb_points
    sc.set_color(colors)
    sizes = np.ones(nb_points) * size
    sc.set_sizes(sizes)
    ax.set_xlabel('Total Deaths',fontsize=14)
    ax.set_ylabel('Total GDP Loss (B)',fontsize=14)

    return fig,ax,sc
def normalize(x,data_min,data_max):
    return (x - data_min) / (data_max - data_min)

def center_vbox(children):
    box_layout = Layout(display='flex',
                flex_flow='column',
                align_items='center',
                width='100%')
    centered_layout = VBox(children=children, layout = box_layout)
    return centered_layout



def run_env_with_actions(actions, env, reset_same_model):

    additional_keys = ('costs', 'constraints')
    # Setup saved values
    episode = dict(zip(additional_keys, [[] for _ in range(len(additional_keys))] ))
    env_states = []
    aggregated_costs = []
    dones = []
    if reset_same_model:
        env.reset_same_model()
    state = env.reset()
    env_states.append(state)

    done = False
    t = 0
    counter = 0
    while not done:
        # Interact
        next_state, agg_cost, done, info = env.step(actions[counter])
        # Save stuff
        state = next_state
        t = env.unwrapped.t
        counter += 1
        aggregated_costs.append(agg_cost)
        env_states.append(state)
        dones.append(done)

        for k in additional_keys:
            episode[k].append(info[k])

    # Form episode dict
    episode.update(env_states=np.array(env_states),
                   aggregated_costs=np.array(aggregated_costs),
                   actions=np.array(actions),
                   dones=np.array(dones))

    aggregated_costs = np.sum(episode['aggregated_costs'])
    costs = np.sum(episode['costs'], axis=0)
    stats = env.unwrapped.get_data()

    return stats, costs

def try_it_ui(checkbox_objects,box_layout):
    number_of_week=52
    number_of_week_per_row=5
    offset_button=10

    weekBox=Box(children=[])
    for i in range(int(number_of_week/number_of_week_per_row)):
        weekBox=VBox([weekBox,Box(checkbox_objects[number_of_week_per_row*(i)+offset_button:
                                                   number_of_week_per_row*(i+1)+offset_button])])
    setBox=Box([checkbox_objects[6]],layout=Layout(display='flex',
                                                   flex_flow='column',
                                                   align_items='center',
                                                   width='100%'))
    runBox = Box([checkbox_objects[8]], layout=Layout(display='flex',
                                                      flex_flow='column',
                                                      align_items='center',
                                                      width='100%'))
    ui=Box(children=[HBox([checkbox_objects[0], checkbox_objects[2], checkbox_objects[1]]),
                     checkbox_objects[2],
                     HBox([checkbox_objects[3], checkbox_objects[2], checkbox_objects[4]]),
                     checkbox_objects[5],
                     setBox,
                     checkbox_objects[7],
                     weekBox,
                     checkbox_objects[7],
                     runBox,
                     checkbox_objects[7],
                     ]
            ,layout=box_layout)
    return ui
def test_layout(algorithm_str,seed,deterministic_model):
    def update_algo_deter(change):
        deterministic_model=change.new
        algorithm, cost_function, env, params = setup_for_replay(folder+to_add , seed, deterministic_model)
        return algorithm, cost_function, env, params
    if seed is None:
        seed = np.random.randint(1e6)
    if algorithm_str == 'DQN':
        to_add = '0.5/'
        folder = get_repo_path() + "/data/data_for_visualization/DQN/"
    elif algorithm_str=='yourself':
        folder = get_repo_path() + "/data/data_for_visualization/NSGA/1/"
        to_add = ''
    else:
        to_add = ''
        folder = get_repo_path() + "/data/data_for_visualization/"+ algorithm_str+ "/1/"
    algorithm, cost_function, env, params = setup_for_replay(folder+to_add , seed, deterministic_model)

    def get_lockdown_stats(stats):
        lockdown = stats['history']['lockdown']
        n_lockdowns = sum(lockdown)
        consecutive_locks = []
        counter = 0
        for a_prev, a in zip(lockdown[:-1], lockdown[1:]):
            if a == 1:
                counter += 1
            else:
                if a_prev == 1:
                    consecutive_locks.append(counter)
                    counter = 0
        if len(consecutive_locks) == 0:
            av_lockdown = 0
        else:
            av_lockdown = np.mean(consecutive_locks)
        nb_lockdowns = len(consecutive_locks)
        return int(n_lockdowns), av_lockdown, int(nb_lockdowns)

    def get_costs(stats):
        costs = np.array([stats['stats_run']['to_plot'][1], stats['stats_run']['to_plot'][4]])
        return costs[:, -1]

    def update_stats(stats, lockdown_stats, costs_stats):

        n_lockdowns, av_lockdown, nb_lockdowns = get_lockdown_stats(stats)
        costs = get_costs(stats)
        lockdown_stats.value = '<font size=3><p><span style="font-weight:500;">Lockdown statistics:</span><br>' + \
                               '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Number of lockdown periods: {}<br>'.format(nb_lockdowns) + \
                               '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Average lockdown length: {:.2f} days<br>'.format(av_lockdown) + \
                               '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Total under lockdown: {} days<br>'.format(n_lockdowns) + \
                               '</p></font>'
        costs_stats.value = '<font size=3><p><span style="font-weight:500;">Cumulative costs:</span><br>' + \
                            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sanitary cost: {} deaths<br>'.format(int(costs[0])) + \
                            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Economic cost: {:.2f} B€.<br>'.format(costs[1]) + \
                            '</p></font>'

    if algorithm_str == 'DQN':
        is_deter=deter_checkbox()
        str_html=algorithm_description(algorithm_str)
        stats, msg = run_env(algorithm, env, first=True)
        fig, lines, plots_i, high, axs = setup_fig_notebook(stats)
        slider = FloatSlider(orientation='horizontal',description='beta:',value=0.5,
                             min=0,
                             max=1,
                             step=0.05,layout={'width': '450px'}
                             )

        slider=slider_setup(slider)
        fig=canvas_setup(fig)
        n_lockdowns, av_lockdown, nb_lockdowns = get_lockdown_stats(stats)
        costs = get_costs(stats)
        lockdown_stats = HTML(value='<font size=3><p><span style="font-weight:500;">Lockdown statistics:</span><br>'
                                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Number of lockdown periods: {}<br>'.format(nb_lockdowns) + \
                                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Average lockdown length: {:.2f} days<br>'.format(av_lockdown) + \
                                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Total under lockdown: {} days'.format(n_lockdowns) + \
                                    '</p></font>')
        fake_stats = HTML(value='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
        costs_stats = HTML(value='<font size=3><p><span style="font-weight:500;">Cumulative costs:</span><br>'
                                 '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sanitary cost: {} deaths<br>'.format(
            int(costs[0])) + \
                                 '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Economic cost: {:.2f} B€.<br>&nbsp;<br>'.format(costs[1]) + \
                                 '</p></font>')

        def update_lines(change):
            beta=slider.value
            deterministic_model=is_deter.value
            algorithm, cost_function, env, params = setup_for_replay(folder + str(beta) + '/', seed, deterministic_model)
            stats, msg = run_env(algorithm, env, goal=np.array([beta]))
            replot_stats(lines, stats, plots_i, cost_function, high)
            update_fig(fig)
            update_stats(stats, lockdown_stats, costs_stats)

        slider.observe(update_lines, names='value')
        is_deter.observe(update_lines,names='value')
        final_layout = center_vbox([str_html,is_deter,slider,fig.canvas, HBox([lockdown_stats, fake_stats, costs_stats])])
        return final_layout
    elif algorithm_str == 'NSGA':
        is_deter=deter_checkbox()
        str_html=algorithm_description(algorithm_str)
        stats, msg = run_env(algorithm, env)
        fig1, lines, plots_i, high, axs = setup_fig_notebook(stats)
        size = 15
        color = "#004ab3"
        color_highlight = "#b30000"

        fig,ax,sc=plot_pareto(algorithm,size,color)
        data = sc.get_offsets().data
        data_max = np.max(data, axis=0)
        data_min = np.min(data, axis=0)
        nb_points = data.shape[0]
        
        def normalize(x):
            return (x - data_min) / (data_max - data_min)

        normalized_data = normalize(data)
        n_lockdowns, av_lockdown, nb_lockdowns = get_lockdown_stats(stats)
        costs = get_costs(stats)
        lockdown_stats = HTML(value='<font size=3><p><span style="font-weight:500;">Lockdown statistics:</span><br>'
                                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Number of lockdown periods: {}<br>'.format(nb_lockdowns) + \
                                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Average lockdown length: {:.2f} days<br>'.format(av_lockdown) + \
                                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Total under lockdown: {} days<br>'.format(n_lockdowns) + \
                                    '</p></font>')

        fake_stats = HTML(value='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
        costs_stats = HTML(value='<font size=3><p><span style="font-weight:500;">Cumulative costs:</span><br>'
                                 '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sanitary cost: {} deaths<br>'.format(
            int(costs[0])) + \
                                 '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Economic cost: {:.2f} B€.<br>&nbsp;<br>'.format(costs[1]) + \
                                 '</p></font>')
        def onclick2(event):
            x = event.xdata
            y = event.ydata

            # find closest in dataset
            point = np.array([x, y])
            normalized_point = normalize(point)
            dists = np.sqrt(np.sum((normalized_point - normalized_data) ** 2, axis=1))
            closest_ind = np.argmin(dists)

            # highlight it
            order = np.concatenate([np.arange(closest_ind), np.arange(closest_ind + 1, nb_points), np.array([closest_ind])])
            sc.set_offsets(data[order])
            sizes = np.ones(nb_points) * size
            sizes[-1] = size * 5
            colors = [color] * nb_points
            colors[-1] = color_highlight
            sc.set_sizes(sizes)  # you can set you markers to different sizes
            sc.set_color(colors)
            # rerun env
            weights = algorithm.res_eval['X'][closest_ind]
            algorithm.policy.set_params(weights)
            stats, msg = run_env(algorithm, env)
            replot_stats(lines, stats, plots_i, cost_function, high)
            print(env.model.stochastic)
            # refresh figure
            update_fig(fig1)
            update_fig(fig)
            update_stats(stats, lockdown_stats, costs_stats)

        def update_deter(change):
            deterministic_model=change.new
            env.model.stochastic = not deterministic_model
            env.model.define_params_and_initial_state_distributions()
        is_deter.observe(update_deter,names='value')
        cid = fig.canvas.mpl_connect('button_press_event', onclick2)
        fig=canvas_setup(fig)
        fig1=canvas_setup(fig1)
        final_layout = center_vbox([str_html,is_deter,fig.canvas, fig1.canvas, HBox([lockdown_stats, fake_stats, costs_stats])])
        return(final_layout)
    elif 'GOAL_DQN' in algorithm_str:
        if cost_function.use_constraints:
            goal = np.array([0.5, 1, 1])
        else:
            goal = np.array([0.5])
        str_html=algorithm_description(algorithm_str)
        
        stats, msg = run_env(algorithm, env, goal, first=True)
        fig, lines, plots_i, high, axs = setup_fig_notebook(stats)

        n_lockdowns, av_lockdown, nb_lockdowns = get_lockdown_stats(stats)
        costs = get_costs(stats)
        lockdown_stats = HTML(value='<font size=3><p><span style="font-weight:500;">Lockdown statistics:</span><br>'
                                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Number of lockdown periods: {}<br>'.format(nb_lockdowns) + \
                                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Average lockdown length: {:.2f} days<br>'.format(av_lockdown) + \
                                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Total under lockdown: {} days<br>'.format(n_lockdowns) + \
                                    '</p></font>')

        fake_stats = HTML(value='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
        costs_stats = HTML(value='<font size=3><p><span style="font-weight:500;">Cumulative costs:</span><br>'
                                 '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sanitary cost: {} deaths<br>'.format(
            int(costs[0])) + \
                                 '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Economic cost: {:.2f} B€.<br>&nbsp;<br>'.format(costs[1]) + \
                                 '</p></font>')

        if cost_function.use_constraints:
            # Plot constraints as dotted line.
            style={'description_width': '150px'}
            M_sanitary = cost_function.costs[0].compute_constraint(1)
            line, = axs[1].plot([0, params['simulation_horizon']],
                                [M_sanitary, M_sanitary],
                                c='k',
                                linestyle='--')
            lines.append(line)
            M_economic = cost_function.costs[1].compute_constraint(1)
            line, = axs[3].plot([0, params['simulation_horizon']],
                                [M_economic, M_economic],
                                c='k',
                                linestyle='--')
            lines.append(line)
            #Define slider
            slider_beta = FloatSlider(orientation='horizontal',
                                            description='beta',
                                            style = style,
                                            value=0.5,
                                            min=0,
                                            max=1,
                                            step=0.05,
                                            layout={'width': '450px'}
                                            )
            slider_M_sanitary = IntSlider(orientation='horizontal',
                                            description='Sanitary constraint',
                                            style = style,
                                            value=62000,
                                            min=1000,
                                            max=62000,
                                            step=5000,
                                            layout={'width': '450px'}
                                            )   
            slider_M_economic = IntSlider(orientation='horizontal',
                                            description='Economic constraint',
                                            style = style,
                                            value=160,
                                            min=20,
                                            max=160,
                                            step=20,
                                            layout={'width': '450px'}
                                            )
            slider_beta=slider_setup(slider_beta)
            slider_M_sanitary=slider_setup(slider_M_sanitary)
            slider_M_economic=slider_setup(slider_M_economic)
            fig=canvas_setup(fig)
            is_deter=deter_checkbox()
            is_deter.style=style
            is_deter.layout.width='200px'


            def update_const(change):
                # normalize constraints
                M_sanitary=slider_M_sanitary.value
                M_economic=slider_M_economic.value
                beta=slider_beta.value
                deterministic_model=is_deter.value
                algorithm, cost_function, env, params = setup_for_replay(folder + to_add, seed, deterministic_model)
                c_sanitary = cost_function.costs[0].compute_normalized_constraint(M_sanitary)
                c_economic = cost_function.costs[1].compute_normalized_constraint(M_economic)
                stats, msg = run_env(algorithm, env, goal=np.array([beta, c_sanitary, c_economic]))
                replot_stats(lines, stats, plots_i, cost_function, high, constraints=[c_sanitary, c_economic])
                update_fig(fig)
                update_stats(stats, lockdown_stats, costs_stats)

            slider_beta.observe(update_const, 'value')
            slider_M_sanitary.observe(update_const, 'value')
            slider_M_economic.observe(update_const, 'value')
            is_deter.observe(update_const,names='value')

            final_layout = center_vbox([str_html,
                                        center_vbox([is_deter,slider_beta,slider_M_sanitary,slider_M_economic]),
                                        fig.canvas, HBox([lockdown_stats, fake_stats, costs_stats])])
            return final_layout
        else :
            is_deter=deter_checkbox()
            slider_goal = FloatSlider(orientation='horizontal',
                                      description='beta:',
                                      value=0.5,
                                      min=0,
                                      max=1,
                                      step=0.05,
                                      layout={'width': '450px'}
                                      )
            slider_goal=slider_setup(slider_goal)


            fig=canvas_setup(fig)

            def update_goal(change):
                beta=slider_goal.value
                deterministic_model=is_deter.value
                algorithm, cost_function, env, params = setup_for_replay(folder + to_add, seed, deterministic_model)
                stats, msg = run_env(algorithm, env, goal=np.array([beta]))
                replot_stats(lines, stats, plots_i, cost_function, high)
                update_fig(fig)
                update_stats(stats, lockdown_stats, costs_stats)

            slider_goal.observe(update_goal, names='value')
            is_deter.observe(update_goal,names='value')
            final_layout = center_vbox([str_html, is_deter, slider_goal,fig.canvas, HBox([lockdown_stats, fake_stats, costs_stats])])
            return final_layout
    elif algorithm_str == 'yourself':
        algorithm, cost_function, env, params = setup_for_replay(folder + to_add, seed, deterministic_model=False)
        style={'description_width': '250px', 'widget_width': '50%'}
        run_eval = True
        n_evals = 10  # number of evaluation rolloutsseed = None  # None picks a random seed
        str_html=algorithm_description(algorithm_str)
        global actions
        actions = get_action_base('never')
        stats, costs = run_env_with_actions(actions,env, reset_same_model=False)
        fig1, lines, plots_i, high, axs = setup_fig_notebook(stats)
        size = 15
        color = "#004ab3"
        color_highlight = "#b30000"
        n_lockdowns, av_lockdown, nb_lockdowns = get_lockdown_stats(stats)
        costs = get_costs(stats)
        lockdown_stats = HTML(value='<font size=3><p><span style="font-weight:500;">Lockdown statistics:</span><br>'
                                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Number of lockdown periods: {}<br>'.format(nb_lockdowns) + \
                                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Average lockdown length: {:.2f} days<br>'.format(av_lockdown) + \
                                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Total under lockdown: {} days<br>'.format(n_lockdowns) + \
                                    '</p></font>')

        fake_stats = HTML(value='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
        costs_stats = HTML(value='<font size=3><p><span style="font-weight:500;">Cumulative costs:</span><br>'
                                 '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sanitary cost: {} deaths<br>'.format(
            int(costs[0])) + \
                                 '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Economic cost: {:.2f} B€.<br>&nbsp;<br>'.format(costs[1]) + \
                                 '</p></font>')

        fig,ax,sc=plot_pareto(algorithm,size,color)
        data = sc.get_offsets().data
        off_sets = sc.get_offsets()
        data_max = np.max(data, axis=0)
        data_min = np.min(data, axis=0)
        nb_points = data.shape[0]
        set_button = Button(value=True,
                                      description='Set to pattern',
                                      disabled=False,
                                      button_style='',  # 'success', 'info', 'warning', 'danger' or ''
                                      layout=Layout(width='30%', height='50px'),
                                      style=style,
                                      tooltip='Click to reset to pattern defined above.',
                                      icon='check'  # (FontAwesome names without the `fa-` prefix)
                                      )

        run_button = Button(value=True,
                            description='Run simulations',
                            disabled=False,
                            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
                            layout=Layout(width='30%', height='50px'),
                            style=style,
                            tooltip='Click to run a simulation with the intervention defined by the checkboxes.',
                            icon='check'  # (FontAwesome names without the `fa-` prefix)
                            )
        start = Dropdown(options=[str(i) for i in range(1, 54)],
                                 value='1',
                                 description="# weeks before pattern starts",
                                 layout=Layout(width='35%', height='30px'),
                                 style=style)

        stop = Dropdown(options=[str(i) for i in range(1, 55)],
                                 value='54',
                                 description="# weeks before pattern stops",
                                 layout=Layout(width='35%', height='30px'),
                                 style=style)

        nb_weeks = Dropdown(options=[str(i) for i in range(0, 54)],
                                    value='0',
                                    description="Duration of lockdown phase (weeks)",
                                    layout=Layout(width='35%', height='30px'),
                                    style=style)

        every = Dropdown(options=[str(i) for i in range(1, 54)],
                                 value='1',
                                 description="Duration of the cycle or period (weeks)",
                                 layout=Layout(width='35%', height='30px'),
                                 style=style)
        fake_stats1 = HTML(value='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
        names = ['start','stop', 'fake', 'nb_weeks', 'every', 'fake', 'set_button', 'fake', 'run_button', 'fake']
        checkbox_objects = [start,stop,fake_stats1, nb_weeks,every, fake_stats1, set_button, fake_stats1, run_button, fake_stats1]
        arg_dict_2 = {names[i]: checkbox for i, checkbox in enumerate(checkbox_objects)}
        for i in range(52):
            desc='Week {}'.format(i + 1)
            checkbox_objects.append(Checkbox(value=False, description=desc))
            names.append(desc)
        arg_dict = {names[i]: checkbox for i, checkbox in enumerate(checkbox_objects)}
        del arg_dict['set_button']
        del arg_dict['run_button']
        box_layout = Layout(overflow_y='auto',
                    #border='3px solid black',
                    #height='450px',
                    display='block',width='950px')
        # ui = Box(children=checkbox_objects, layout=box_layout)
        ui=try_it_ui(checkbox_objects,box_layout)
        # global ACT
        # ACT = np.zeros([52])
        def update_try(**kwargs):
            # start=int(kwargs['start'])-1
            # stop=int(kwargs['stop'])-1
            # nb_weeks=int(kwargs['nb_weeks'])
            # every=int(kwargs['every'])
            # action_str = str(nb_weeks) + '_' + str(every)
            # set_button=kwargs['set_button']
            # t_i = time.time()
            # actions = get_action_base(action_str, start, stop)
            # if not np.all(ACT == actions):
            #     assert False
            #     ACT = actions.copy()
            # if set_button:
            #     for i in range(52):
            #         checkbox_objects[8+i].value = bool(actions[i])
            #
            actions = np.array([int(kwargs['Week {}'.format(i+1)]) for i in range(52)])
            # for i in range(52):
            #     actions[i] = int(kwargs['Week {}'.format(i+1)])
            # stats, costs = run_env_with_actions(actions, env, reset_same_model=deterministic_model)
            # # if run_eval:
            # #     all_costs = [run_env_with_actions(actions, env, reset_same_model=False)[1] for _ in range(n_evals)]
            # #     all_costs = np.array(all_costs)
            # #     print(all_costs)
            # #     means = all_costs.mean(axis=0)
            # #     x, y = means
            # #     stds = all_costs.std(axis=0)
            # #     # msg = '\nEvaluation (over {} seeds):'.format(n_evals)
            # #     # msg += '\n\t Death toll: {} +/- {}'.format(int(means[0]), int(stds[0]))
            # #     # msg += '\n\t Economic cost: {:.2f} +/- {:.2f} B€.'.format(int(means[1]), int(stds[1]))
            # #     # print(msg)
            # # else:
            # x, y = costs
            # # print('\nDeath toll: {}, Economic cost: {:.2f} B€.'.format(int(costs[0]), costs[1]))
            # replot_stats(lines, stats, plots_i, cost_function, high)
            #
            # # update PAreto:
            # new_offsets = np.concatenate([off_sets, np.array([[x, y]])], axis=0)
            # sc.set_offsets(new_offsets)
            # new_colors = [color] * nb_points + [color_highlight]
            # sc.set_color(new_colors)
            # new_sizes = [size] * nb_points + [size * 2]
            # sc.set_sizes(new_sizes)
            #
            # update_fig(fig)
            # update_fig(fig1)
            # update_stats(stats, lockdown_stats, costs_stats)
            return actions

        def update_set_pattern(b):
            start_value = int(start.value) - 1
            stop_value = int(stop.value) - 1
            nb_weeks_value = int(nb_weeks.value)
            every_value = int(every.value)

            # start = int(kwargs['start']) - 1
            # stop = int(kwargs['stop']) - 1
            # nb_weeks = int(kwargs['nb_weeks'])
            # every = int(kwargs['every'])
            action_str = str(nb_weeks_value) + '_' + str(every_value)
            actions = get_action_base(action_str, start_value, stop_value)
            for i in range(52):
                checkbox_objects[10 + i].value = bool(actions[i])

        def run_simulation(b):
            actions = np.array([int(cb.value) for cb in checkbox_objects[10:]])
            stats, costs = run_env_with_actions(actions, env, reset_same_model=deterministic_model)
            if run_eval:
                all_costs = [run_env_with_actions(actions, env, reset_same_model=False)[1] for _ in range(n_evals)]
                all_costs = np.array(all_costs)
                means = all_costs.mean(axis=0)
                x, y = means
            else:
                x, y = costs
            # print('\nDeath toll: {}, Economic cost: {:.2f} B€.'.format(int(costs[0]), costs[1]))
            replot_stats(lines, stats, plots_i, cost_function, high)

            # update PAreto:
            new_offsets = np.concatenate([off_sets, np.array([[x, y]])], axis=0)
            sc.set_offsets(new_offsets)
            new_colors = [color] * nb_points + [color_highlight]
            sc.set_color(new_colors)
            new_sizes = [size] * nb_points + [size * 2]
            sc.set_sizes(new_sizes)

            update_fig(fig)
            update_fig(fig1)
            update_stats(stats, lockdown_stats, costs_stats)
            return actions

        out = interactive_output(update_try, arg_dict)
        # out2 = interactive_output(update_set_pattern, arg_dict_2)
        set_button.on_click(update_set_pattern)
        run_button.on_click(run_simulation)

        fig=canvas_setup(fig)
        fig1=canvas_setup(fig1)
        final_layout = center_vbox([str_html,ui,fig.canvas, fig1.canvas, HBox([lockdown_stats, fake_stats, costs_stats])])
        return final_layout
    else:
        raise NotImplementedError
