import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import cv2


if __name__ == '__main__':
    os.chdir("D:/GIT_REPOS/2021-NCKU_NN/Project3_final/group1_8")

    df_full = pd.read_csv('df_full.csv')
    group_code = 8
    _df = df_full.loc[df_full['group'] ==
                      group_code][['x_c', 'y_c', 'vx_filter']]
    # _vdf = df_full.loc[df_full['group'] == group_code][['vx', 'vy']]
    X = np.tile(np.arange(_df.shape[0]), (4, 1)).T
    Y = _df.to_numpy()

    # For cursor position
    init_x = _df.head(1).index.tolist()[0]
    init_y = _df.iloc[0, 0]
    img_id_max = df_full.tail(1).index.tolist()[0]
    print(img_id_max)

    # Show Graph
    fig = plt.figure(figsize=(30, 10))
    ax = sns.scatterplot(data=_df)  # , markers=['.', '.']
    plt.suptitle(f'Group {group_code}', fontsize='20')
    ax.set_title('"" selected.')
    ax.legend(fontsize='20')
    ax.axhline(y=1920, color='b', linestyle='--', linewidth=0.5)
    ax.axhline(y=1080, color='r', linestyle='--', linewidth=0.5)
    ax.axhline(y=1000, color='black', linestyle='--', linewidth=0.5)
    # move to second monitor and maximize window
    plt.get_current_fig_manager().window.move(2000, 0)
    plt.get_current_fig_manager().window.showMaximized()
    # plt.get_current_fig_manager().full_screen_toggle()

    hover_hint = 'HOVER'
    select_hint = 'SELECT'
    mx = ax.axvline(x=init_x, color='black', linewidth=0.3)
    my = ax.axhline(y=init_y, color='black', linewidth=0.3)
    plt.text(100, 100, select_hint, fontsize=12)

    def hover(event):
        if event.xdata is not None and event.ydata is not None:
            mx.set_xdata(x=event.xdata)
            my.set_ydata(y=event.ydata)
            img_id = int(event.xdata)
            if 0 <= img_id <= img_id_max:
                img_name = df_full['filename'].loc[img_id]
                hover_hint = f'"{img_name}"'
            else:
                hover_hint = 'Nothing'
                print(f'{img_id} exceeds boundary!')
            ax.set_title(select_hint + '\n' + hover_hint)
            fig.canvas.draw()

    def onclick(event):
        if event.dblclick and event.xdata is None or event.ydata is None:
            return
        # print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
        #       ('double' if event.dblclick else 'single', event.button,
        #        event.x, event.y, event.xdata, event.ydata))
        img_id = int(event.xdata)
        if 0 <= img_id <= img_id_max:
            img_name = df_full['filename'].loc[img_id]
            select_hint = f'"{img_name}" has been selected.'
        else:
            select_hint = f'Nothing has been selected.'
            print(f'{img_id} exceeds boundary!')
        ax.set_title(select_hint + '\n' + hover_hint)
        fig.canvas.draw()

    fig.canvas.mpl_connect("motion_notify_event", hover)
    fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    print('TERMINATED')
