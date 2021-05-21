import base64
from io import BytesIO
import matplotlib.pyplot as plt
from instrument.models import Instrument
import seaborn as sns


def get_graph():
    buffer=BytesIO()
    plt.savefig(buffer,format="png")
    buffer.seek(0)
    image_png=buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_chart(chart_type,data,**kwargs):
    plt.switch_backend("AGG")
    fig = plt.figure(figsize=(10,4))


    if chart_type == "#1":
        # plt.bar(data['region_id'],data['invested'])
        x_axis=kwargs.get('x')
        y_axis=kwargs.get('y')
        sns.barplot(x=x_axis,y=y_axis,data=data)

    elif chart_type == "#2":
        labels=kwargs.get('labels')
        y_axis=kwargs.get('y')
        plt.pie(data=data,x=y_axis, labels=labels)

    elif chart_type == "#3":
        x_axis=kwargs.get('x')
        y_axis=kwargs.get('y')
        plt.plot(data[x_axis],data[y_axis],color='green',marker='o', linestyle="dashed")


    plt.tight_layout()
    chart=get_graph()
    return chart