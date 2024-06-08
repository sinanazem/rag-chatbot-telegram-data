import plotly.graph_objects as go

def plot_top_users(top_users):
    # Extract data for plotting
    users = [user['user'] for user in top_users]
    message_counts = [user['message_count'] for user in top_users]

    # Define color scale based on message count
    colorscale = 'Viridis'  # You can choose from various color scales

    # Create the bar chart
    fig = go.Figure(data=[
        go.Bar(name='Message Count', x=users, y=message_counts, marker=dict(color=message_counts, colorscale=colorscale))
    ])

    # Update layout for better readability
    fig.update_layout(
        title='Top Users by Message Count',
        xaxis_title='User',
        yaxis_title='Message Count',
        xaxis_tickangle=-45,
        template='plotly_white'
    )

    # Show the plot
    return fig

def plot_top_users_donut(top_users):
    # Extract data for plotting
    users = [user['user'] if user['user'] is not None else 'Unknown' for user in top_users]
    message_counts = [user['message_count'] for user in top_users]

    # Create the donut chart
    fig = go.Figure(data=[
        go.Pie(
            labels=users,
            values=message_counts,
            hole=0.4,  # Creates the donut hole
            textinfo='label+percent',
            hoverinfo='label+value'
        )
    ])

    # Update layout for better readability
    fig.update_layout(
        title='Top Users by Message Count',
        template='plotly_white'
    )

    # Show the plot
    return fig



def plot_message_counts(message_counts):
    # Extract data for plotting
    dates = [item['date'] for item in message_counts]
    counts = [item['count'] for item in message_counts]

    # Create the line chart
    fig = go.Figure(data=[
        go.Scatter(name='Message Count', x=dates, y=counts, mode='lines+markers')
    ])

    # Update layout for better readability
    fig.update_layout(
        title='Number of Messages Over Time',
        xaxis_title='Date',
        yaxis_title='Message Count',
        xaxis_tickangle=-45,
        template='plotly_white'
    )

    # Show the plot
    return fig

import plotly.graph_objects as go

def plot_question_counts(question_counts):
    # Extract data for plotting
    users = [item['user'] for item in question_counts]
    question_counts_data = [item['question_count'] for item in question_counts]

    # Define color scale based on the "strength" of question count
    colorscale = 'Viridis'  # You can choose from various color scales

    # Create the bar chart
    fig = go.Figure(data=[
        go.Bar(name='Question Count', x=users, y=question_counts_data, marker=dict(color=question_counts_data, colorscale=colorscale))
    ])

    # Update layout for better readability
    fig.update_layout(
        title='Number of Questions Asked by Users',
        xaxis_title='User',
        yaxis_title='Question Count',
        xaxis_tickangle=-45,
        template='plotly_white'
    )

    # Show the plot
    return fig
