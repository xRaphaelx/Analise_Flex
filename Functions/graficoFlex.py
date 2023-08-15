import pandas as pd
import matplotlib.pyplot as plt

linesStyles = {0:'-',1:'--',2:'-.'}

def geraGraficoFlex(df,dfRealizado):

    fig,ax=plt.subplots(figsize=(14, 10))


    # st.write(df[['month','contractedVolumeMwm']])
    # st.write(df[['month','maxFlexVolumeMwm']])
    # st.write(df[['month','minFlexVolumeMwm']])
    # st.write(dfRealizado[['month','finalVolumeMwm']])
    # st.line_chart(df[['mesAno','contractedVolumeMwm']],x='mesAno',y='contractedVolumeMwm')

    contratos = pd.unique(df['code'])
    for x,contrato in enumerate(contratos):

        dfAux = df[df['code']==contrato]
        dfAuxRealizado= dfRealizado[dfRealizado['code']==contrato]

        ax.plot(dfAux['mesAno'],dfAux['contractedVolumeMwm'],label=f'Volume Contratado',lw=2.5,ls=linesStyles[x],color='green')
        ax.plot(dfAux['mesAno'],dfAux['maxFlexVolumeMwm'],label=f'Volume Maximo Flex',lw=2.5,ls=linesStyles[x],color='blue')
        ax.plot(dfAux['mesAno'],dfAux['minFlexVolumeMwm'],label=f'Volume Minimo Flex',lw=2.5,ls=linesStyles[x],color='red')
        ax.plot(dfAuxRealizado['mesAno'],dfAuxRealizado['finalVolumeMwm'],label=f'Volume Entregado',lw=2.5,ls=linesStyles[x],color='black')


    handles, labels = ax.get_legend_handles_labels()
    ax.legend(reversed(handles), reversed(labels),loc='center', bbox_to_anchor=(0.51, -0.13),ncol=5).get_frame().set_alpha(0)

    ax.set_ylabel('MWmed') #titulo eixo y
    ax.set_xlabel('Data') #titulo eixo x
    # ax.set_title(f'Series Newave - {titulo}\nCMO - {sub}',pad=20,size=15) # titulo grafico

    # ax.xaxis.set_ticks(dfSubMedia['dataSerie'])

    # ax.set_xlim(min(dfSubMedia['dataSerie']),max(dfSubMedia['dataSerie']))
    # ax.set_ylim(0,800)
    # ax.set_xticklabels(dfSubMedia['dataSerie'].apply(lambda x: date2monthYear(x)),rotation = 45)


    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.grid(axis='y',ls = '-.', lw = 0.9)
    ax.grid(axis='x',ls = '-.', lw = 0.9)

    return fig

    plt.savefig(f'Graficos/50seriesCMO_{sub}.jpg',dpi=200,bbox_inches='tight')
    plt.close(fig)
