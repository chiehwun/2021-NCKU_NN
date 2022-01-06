import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
from PIL import Image
ABS_IMG_PATH = 'D:/GIT_REPOS/2021-NCKU_NN/Project3_final/group1_8/Images/'

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

    ##### Show Graph #####
    # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(
    #     10, 4), gridspec_kw={'width_ratios': [4, 1]})
    fig, axd = plt.subplot_mosaic([['graph', 'info'],
                                   ['graph', 'img']], figsize=(10, 4), gridspec_kw={'width_ratios': [3, 2]})
    ax1 = axd['graph']
    ax2 = axd['info']
    ax3 = axd['img']
    fig.tight_layout()
    plt.subplots_adjust(left=None, bottom=None, right=None,
                        top=None, wspace=0.05, hspace=0)
    # plt.show()
    # exit(0)
    plt.suptitle(f'Group {group_code}', fontsize='20')

    # scatter plot
    sns.scatterplot(ax=ax1, data=_df)  # , markers=['.', '.']
    ax1.axhline(y=1920, color='b', linestyle='--', linewidth=0.5)
    ax1.axhline(y=1080, color='r', linestyle='--', linewidth=0.5)
    ax1.axhline(y=1000, color='black', linestyle='--', linewidth=0.5)

    # Dynamic Object
    mx = ax1.axvline(x=init_x, color='black', linewidth=0.3)
    my = ax1.axhline(y=init_y, color='black', linewidth=0.3)

    # axis 1 labels
    ax1.set_xlabel('Image Sequence')

    # axis 2,3
    ax3.set_title('selected image')
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax3.set_xticks([])
    ax3.set_yticks([])

    # notes axis 2
    hover_hint = 'HOVER'
    select_hint = 'SELECT'
    bb_str = '(,)'
    ax2.spines[['top', 'right', 'bottom', 'left']].set_visible(False)
    hh = ax2.text(0, 1, hover_hint, ha='left', va='top', fontsize=15)
    ss = ax2.text(0, 0.9, select_hint,
                  ha='left', va='top', fontsize=15)
    bb = ax2.text(0, 0.8, bb_str, ha='left', va='top', fontsize=15)

    def coord_cnv(img_id):
        xmin, ymax, xmax, ymin = df_full.iloc[img_id, 6:10].to_numpy()
        dx = xmax - xmin
        dy = ymax - ymin
        xl = xmin
        yl = 1080 - ymax
        return (xl, yl, dx, dy)

    # Test
    img_path = ABS_IMG_PATH + 'group08_01248.jpg'
    im = Image.open(img_path)
    ax3.imshow(im)
    xl, yl, dx, dy = coord_cnv(37242)
    box = ax3.add_patch(patches.Rectangle(
        (xl, yl), dx, dy, edgecolor='red', fill=False))

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
            hh.set_text(hover_hint)
            fig.canvas.draw_idle()

    def onclick(event):
        if event.dblclick and event.xdata is None or event.ydata is None:
            return
        # print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
        #       ('double' if event.dblclick else 'single', event.button,
        #        event.x, event.y, event.xdata, event.ydata))
        img_id = int(event.xdata)
        if 0 <= img_id <= img_id_max:  # img exists
            img_name = df_full['filename'].loc[img_id]
            select_hint = f'"{img_name}" has been selected.'
            img_path = ABS_IMG_PATH + img_name
            im = Image.open(img_path)
            if df_full.iloc[img_id, 0]:  # bounding bix exist?
                xl, yl, dx, dy = coord_cnv(img_id)
                box.set_visible(True)
                box.set_bounds(xl, yl, dx, dy)
                bb_str = f'({xl}, {yl}, {dx}, {dy})'
            else:
                box.set_visible(False)
                bb_str = '(,)'
            ax3.imshow(im)
        else:
            select_hint = f'Nothing has been selected.'
            print(f'{img_id} exceeds boundary!')
        ss.set_text(select_hint)
        bb.set_text(bb_str)
        fig.canvas.draw()

    fig.canvas.mpl_connect("motion_notify_event", hover)
    fig.canvas.mpl_connect('button_press_event', onclick)

    # move to second monitor and maximize window
    plt.get_current_fig_manager().window.move(2000, 0)
    plt.get_current_fig_manager().window.showMaximized()
    # plt.get_current_fig_manager().full_screen_toggle()
    plt.show()
    print('TERMINATED')
