import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
low = df['value'].quantile(0.025)
high = df['value'].quantile(0.975)
df = df[(df['value'] >= low) & (df['value'] <= high)]


def draw_line_plot():
    # Draw line plot
    x = df.index
    y = df['value']
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    fig = plt.gcf()
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar_plot = df.copy()
    df_bar_plot['month'] = df_bar_plot.index.month
    df_bar_plot['month name'] = df_bar_plot['month'].apply(lambda x: pd.to_datetime(x, format='%m').strftime('%B'))
    df_bar_plot['year'] = df_bar_plot.index.year
    df_bar = df_bar_plot.groupby(['year', 'month name'])['value'].mean().unstack()
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
    ]
    df_bar = df_bar[month_order]
    
    # Draw bar plot
    fig, ax = plt.subplots(figsize=(12, 8))
    df_bar.plot(kind='bar', ax=ax)
    
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months')
    plt.xticks(rotation=0, ha='center')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    month_order = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    df_box['month'] = pd.Categorical(df_box['month'], categories=month_order ,ordered=True)

    # Draw box plots (using Seaborn)
    # first_plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.boxplot(x=df_box['year'], y=df_box['value'], data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_ylabel('Page Views')
    axes[0].set_xlabel('Year')

    # second_boxplot
    sns.boxplot(x=df_box['month'], y=df_box['value'], data=df_box, ax=axes[1], color='green')
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_ylabel('Page Views')
    axes[1].set_xlabel('Month')
    plt.grid()


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
