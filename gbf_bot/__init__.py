from os.path import dirname, join

__all__ = []

package_root = dirname(__file__)
images_dir = join(package_root, 'images')
buttons = lambda x: join(images_dir, 'buttons', x)
