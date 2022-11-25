import io
import json
import boto3
from matplotlib import pyplot
from matplotlib.legend_handler import HandlerTuple
from matplotlib import cm

NS_TO_MS = 1000000

def lambda_handler(event, context):
    """
    :param event: json input from apollo
    :param context: none
    :return: statusCode
    """
    json_input = json.loads(event["body"])
    bucket_url = json_input["bucket"]

    # all values in nano-seconds
    start = json_input["start"]/NS_TO_MS  #int
    stop = [x/NS_TO_MS for x in json_input["stop"]]  #list

    runtime_fetchImage = json_input["runtime_fetchImage"]/NS_TO_MS  #int
    runtime_recognizeFaces = [x / NS_TO_MS for x in json_input["runtime_recognizeFaces"]]  # list
    runtime_cropSortFaces = [x / NS_TO_MS for x in json_input["runtime_cropSortFaces"]]  # list
    runtime_createCollage = [x / NS_TO_MS for x in json_input["runtime_createCollage"]]  # list

    start_recognizeFaces = [x / NS_TO_MS - start for x in json_input["start_recognizeFaces"]]  # list
    start_cropSortFaces = [x / NS_TO_MS - start for x in json_input["start_cropSortFaces"]]  # list
    start_createCollage = [x / NS_TO_MS - start for x in json_input["start_createCollage"]]  # list

    # lists of input for easier iterating
    runtime_list = [runtime_recognizeFaces,runtime_cropSortFaces,runtime_createCollage]
    start_list = [start_recognizeFaces,start_cropSortFaces,start_createCollage]
    runtime_labels = ["Total Runtime",
                      "Runtime fetchImage",
                      "Runtime recognizeFaces",
                      "Runtime cropSortFaces",
                      "Runtime createCollage"]
    total_runtime = max(stop) - start

    """
    Plotting the values
    """
    plt, ax = pyplot.subplots(1, 1)
    X = 1
    t = ax.bar(X - 0.1, total_runtime, color="grey", width=1, linewidth=1.0, edgecolor="black")
    rf = ax.bar(X - 0.1, runtime_fetchImage, color="blue", width=1, linewidth=1.0, edgecolor="black")

    bottom = runtime_fetchImage
    rts = [t, rf]
    for i, l in enumerate(runtime_list):
        width = 1 / len(l)
        offset = len(l) / 2 * width if len(l) % 2 > 0 else len(l) / 2 * width - 0.15
        print(width, offset)
        color = cm.hsv(i / 16 * len(runtime_list))

        temp_tup = ()
        for j, runtime in enumerate(l):
            tmp = ax.bar(X - offset + j * width, runtime, width=width, bottom=start_list[i][j], linewidth=1.0,
                         edgecolor="black", color=color, align="center")
            temp_tup += (tmp,)
        rts.append(temp_tup)
        bottom += max(l)

    for i, rect in enumerate(ax.patches):
        ax.annotate(xy=(rect.get_x() + rect.get_width() / 2.,
                        int(rect.get_y() + rect.get_height() / 2) if i > 0 else int(
                            rect.get_height() + rect.get_height() / 50)),
                    ha='center',
                    va='center',
                    xytext=(0, 0),
                    textcoords='offset points',
                    text=f"{rect.get_height()}ms")

    ax.legend(rts, runtime_labels, handler_map={tuple: HandlerTuple()}, bbox_to_anchor=(1, 1), loc="upper left")
    ax.set_ylabel("Runtime in Milliseconds")
    ax.set_xlabel("Workflow")
    ax.set_xticks([])

    """
    Uploading Figure
    """
    client = boto3.client('s3')
    with io.BytesIO as tmp_fig:
        plt.savefig(tmp_fig, format="png")
        tmp_fig.seek(0)

        client.upload_fileobj(
            tmp_fig,
            bucket_url,
            f"runtimeFigure_{id(tmp_fig)}.png")

    return {
        "statusCode": 200,
        "body": {"statusCode":200}
    }