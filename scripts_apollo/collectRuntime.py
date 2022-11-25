import io
import json
import boto3
from matplotlib import pyplot
from matplotlib.legend_handler import HandlerTuple
from matplotlib import cm

NS_TO_MS = 1000000

def lambda_handler(event, context):
    json_input = json.loads(event["body"])

    bucket_url = json_input["bucket"]
    #all values in nano-seconds
    start = json_input["start"]/NS_TO_MS  #int
    stop = [x/NS_TO_MS for x in json_input["stop"]]  #list
    runtime_fetchImage = json_input["runtime_fetchImage"]/NS_TO_MS  #int
    runtime_recognizeFaces = [x/NS_TO_MS for x in json_input["runtime_recognizeFaces"]]  #list
    runtime_cropSortFaces = [x/NS_TO_MS for x in json_input["runtime_cropSortFaces"]]  #list
    runtime_createCollage = [x/NS_TO_MS for x in json_input["runtime_createCollage"]]  #list

    runtime_list = [runtime_recognizeFaces,runtime_cropSortFaces,runtime_createCollage]
    runtime_labels = ["Total Runtime",
                      "Runtime fetchImage",
                      "Runtime recognizeFaces",
                      "Runtime cropSortFaces",
                      "Runtime createCollage"]

    total_runtime = max(stop) - start

    plt, ax = pyplot.subplots(1,1)
    X = "Config"
    t = ax.bar(X, total_runtime, c="grey")
    rf = ax.bar(X, runtime_fetchImage, c="r")

    bottom = runtime_fetchImage
    rts = [t, rf]
    for i, l in enumerate(runtime_list):
        width = 1/len(l)
        color = cm.hsv(i / len(runtime_list))

        temp_tup = ()
        for j, runtime in enumerate(l):
            tmp = ax.bar(X + j * width, runtime, width=width, c=color, bottom=bottom, linewidth=0.1, align="center")
            temp_tup += (tmp,)
        rts.append(temp_tup)
        bottom += max(l)

    ax.legend(rts, runtime_labels, handler_map={tuple: HandlerTuple(ndivide=None)})
    ax.set_ylabel("Runtime in Milliseconds")

    client = boto3.client('s3')
    with io.BytesIO as tmp_fig:
        plt.savefig(tmp_fig, format="png")
        tmp_fig.seek(0)

        client.upload_fileobj(
            tmp_fig,
            bucket_url,
            f"runtimeFigure.png")

    return {
        "statusCode": 200,
        "body": {"statusCode":200}
    }