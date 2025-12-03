import pandas as pd
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json
from pymongo.collection import Collection
import plotly.io as pio
from datetime import datetime
import os

def create_graph(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> str:
    """
    Generates a Plotly Line chart for a single measurement column.

    Args:
        df (pd.DataFrame): The dataframe containing the time series data.
        x_col (str): The name of the timestamp column.
        y_col (str): The name of the measurement column to plot.
        title (str): The title for the graph.

    Returns:
        str: The graph object encoded as a JSON string.
    """
    # Check if the DataFrame has enough data points to plot
    if df.empty or x_col not in df.columns or y_col not in df.columns:
        print(f"INFO: No data found in dataframe '{df}'.")
        # Create a placeholder empty figure if data is missing
        fig = px.scatter(title=f"{title} - No Data Available")
        fig.update_layout(
            template="plotly_dark",
            xaxis={'visible': False},
            yaxis={'visible': False}
        )
        return pio.to_json(fig)

    # Creation of Plotly figure
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        title=title,
        line_shape='spline'
    )

    fig.update_traces(
        mode='lines+markers',
        marker=dict(size=5, line=dict(width=1, color='Red'))
    )


    # Customizations
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=40, r=20, t=50, b=20),
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title=y_col.replace('_', ' ').title(),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    # graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)
    # return graph_json

    # filename = None
    # if filename is None:
    #     timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    #     filename = f"{y_col}_graph_{timestamp_str}.png"
    #
    # fig.write_image(filename)
    res = pio.to_json(fig, pretty=True)
    print(res)
    return res


# def create_graph(df: pd.DataFrame, x_col: str, y_col: str, title: str, output_dir: str = 'graphs') -> str:
#     """
#     Generates a Plotly Line chart and saves it as an interactive HTML file.
#
#     Args:
#         df (pd.DataFrame): The dataframe containing the time series data.
#         x_col (str): The name of the timestamp column.
#         y_col (str): The name of the measurement column to plot.
#         title (str): The title for the graph.
#         output_dir (str): The directory where the HTML file should be saved.
#
#     Returns:
#         str: The path to the generated HTML file relative to the application root.
#     """
#     # Define the output path for the HTML file
#     file_name = f"{y_col.lower()}_graph.html"
#     filepath = os.path.join(output_dir, file_name)
#
#     # Check if the DataFrame has enough data points to plot
#     if df.empty or x_col not in df.columns or y_col not in df.columns:
#         print(f"INFO: No data found in dataframe for {y_col}.")
#         # Create a placeholder empty figure if data is missing
#         fig = px.scatter(title=f"{title} - No Data Available")
#         fig.update_layout(
#             template="plotly_dark",
#             xaxis={'visible': False},
#             yaxis={'visible': False}
#         )
#     else:
#         # Creation of Plotly figure
#         fig = px.line(
#             df,
#             x=x_col,
#             y=y_col,
#             title=title,
#             line_shape='spline'
#         )
#
#         fig.update_traces(
#             mode='lines+markers',
#             marker=dict(size=5, line=dict(width=1, color='Red'))
#         )
#
#
#         # Customizations
#         fig.update_layout(
#             template="plotly_dark",
#             margin=dict(l=40, r=20, t=50, b=20),
#             xaxis_title=x_col.replace('_', ' ').title(),
#             yaxis_title=y_col.replace('_', ' ').title(),
#             xaxis=dict(showgrid=False),
#             yaxis=dict(showgrid=False)
#         )
#
#     # Save the figure as a standalone HTML file
#     # include_plotlyjs='cdn' ensures Plotly.js is loaded from a CDN inside the file.
#     fig.write_html(filepath, full_html=True, include_plotlyjs='cdn')
#
#     print(f"Graph saved to {filepath}")
#     return filepath




def get_telemetry_measurements(lines: int, collection: Collection) -> pd.DataFrame:
    try:
        cursor = collection.find().sort('timestamp', -1).limit(lines)
        data_list =list(cursor)
        if not data_list:
            print(f"INFO: No data found in collection '{collection.name}'.")
            return pd.DataFrame()

        df = pd.DataFrame(data_list)
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])

        df = df.iloc[::-1].reset_index(drop=True)

        if '_id' in df.columns:
            df = df.drop(columns=['_id'])

        return df
    except Exception as e:
        print(f"An error occurred during data retrieval from MongoDB: {e}")
        return pd.DataFrame()




