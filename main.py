import random
import matplotlib.pyplot as plt
import numpy as np
import sys
import BST, AVL, RB

sys.setrecursionlimit(10000)

"""1.	Реализовать бинарное дерево поиска (BST) и следующие операции:
•	поиск;
•	вставка;
•	удаление;
•	поиск максимума;
•	поиск минимума;
•	прямой/центрированный/обратный обход;
•	обход в ширину.
2.	Реализовать на основе BST АВЛ дерево, дополнив исходную
 структуру/класс и операция вставки/удаления.
3.	Реализовать на основе BST красно-черное дерево, дополнив исходную
 структуру/класс и операция вставки/удаления.
4.	Получить экспериментальную зависимость высоты BST от количества ключей,
 при условии, что значение ключа - случайная величина, распределенная равномерно.
  (Не забудьте, что значения ключей в BST не повторяются).
Вывести полученные результаты на графики Какая асимптотика функции высоты h(n)
 наблюдается у двоичного дерева поиска?
5.	Получить экспериментальную зависимость высоты АВЛ и красно-черного дерева от
 количества ключей, при условии, что значение ключа - случайная величина, распределенная равномерно.
Вывести полученные результаты на графики. Сравнить с графиками теоретической
 верхней и нижней оценкой высоты.
6.	Получить экспериментальную зависимость высоты АВЛ и красно-черного дерева
 от количества ключей, при условии, что значения ключей монотонно возрастают.
Вывести полученные результаты на графики. Сравнить с графиками теоретической
 верхней и нижней оценкой высоты.
"""


def test_tree(tree_class, keys):
    tree = tree_class()
    for key in keys:
        tree.insert(key)
    return tree.get_height()


def experiment_random_keys(tree_classes, n_values, trials=10):
    results = {}
    for tree_class in tree_classes:
        results[tree_class.__name__] = []

    for n in n_values:
        print(f"Testing n={n}")
        for tree_class in tree_classes:
            heights = []
            for _ in range(trials):
                keys = random.sample(range(n * 10), n)
                height = test_tree(tree_class, keys)
                heights.append(height)

            avg_height = sum(heights) / len(heights)
            results[tree_class.__name__].append(avg_height)

    return results


def experiment_sorted_keys(tree_classes, n_values):
    results = {}
    for tree_class in tree_classes:
        results[tree_class.__name__] = []

    for n in n_values:
        print(f"Testing sorted n={n}")
        for tree_class in tree_classes:
            keys = list(range(n))
            height = test_tree(tree_class, keys)
            results[tree_class.__name__].append(height)

    return results


def plot_results(n_values, results_dict, title, log_scale=False):
    plt.figure(figsize=(10, 6))

    for name, heights in results_dict.items():
        plt.plot(n_values, heights, marker='o', label=name)

    if log_scale:
        plt.yscale('log')
        plt.xscale('log')

    plt.xlabel('Количество ключей (n)')
    plt.ylabel('Высота дерева')
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()


def plot_comparison(n_values, bst_results, avl_results, rb_results, title):
    plt.figure(figsize=(10, 6))

    n_array = np.array(n_values)

    # bst_max = n_array  # O(n) в худшем случае
    avl_max = 1.44 * np.log2(n_array + 2) - 0.328  # Верхняя оценка для AVL
    rb_max = 2 * np.log2(n_array + 1)  # Верхняя оценка для красно-черного

    # bst_min = np.log2(n_array)
    avl_min = np.log2(n_array + 1) - 1
    rb_min = np.log2(n_array + 1)

    plt.plot(n_values, bst_results, marker='o', label='BST (эксперимент)')
    plt.plot(n_values, avl_results, marker='s', label='AVL (эксперимент)')
    plt.plot(n_values, rb_results, marker='^', label='КЧД (эксперимент)')

    plt.plot(n_values, avl_max, '--', label='AVL верхняя граница')
    plt.plot(n_values, rb_max, '--', label='КЧД верхняя граница')

    plt.plot(n_values, avl_min, '--', label='AVL нижня граница')
    plt.plot(n_values, rb_min, '--', label='КЧД нижняя граница')

    plt.xlabel('Количество ключей (n)')
    plt.ylabel('Высота дерева')
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()


def main():
    print("Эксперимент 1 (Случайные ключи)")
    tree_classes_random = [BST.BST, AVL.AVLTree, RB.RedBlackTree]
    n_values_random = [100, 500, 1000, 1500, 2000, 3000, 5000, 10000, 20000]
    random_results = experiment_random_keys(tree_classes_random, n_values_random, trials=5)

    print("\nЭксперимент 2 (Отсортированные ключи)")
    tree_classes_sorted = [AVL.AVLTree, RB.RedBlackTree]
    n_values_sorted = [100, 500, 1000, 1500, 2000, 3000, 5000, 10000, 20000]
    sorted_results = experiment_sorted_keys(tree_classes_sorted, n_values_sorted)

    plot_results(n_values_random, random_results, "Высота деревьев для случайных ключей")
    plot_results(n_values_sorted, sorted_results, "Высота деревьев для отсортированных ключей")

    print("\nСРАВНЕНИЕ")
    plot_comparison(
        n_values_random,
        random_results['BST'],
        random_results['AVLTree'],
        random_results['RedBlackTree'],
        "Сравнение с теоретическими оценками (случайные ключи)"
    )

    print("\nРЕЗУЛЬТАТЫ ДЛЯ СЛУЧАЙНЫХ КЛЮЧЕЙ")
    print("n\tBST\tAVL\tКЧД")
    for i, n in enumerate(n_values_random):
        print(
            f"{n}\t{random_results['BST'][i]:.1f}"
            f"\t{random_results['AVLTree'][i]:.1f}"
            f"\t{random_results['RedBlackTree'][i]:.1f}")

    print("\nРЕЗУЛЬТАТЫ ДЛЯ ОТСОРТИРОВАННЫХ КЛЮЧЕЙ")
    print("n\tBST\tAVL\tКЧД")
    for i, n in enumerate(n_values_random):
        print(
            f"\t{sorted_results['AVLTree'][i]:.1f}"
            f"\t{sorted_results['RedBlackTree'][i]:.1f}")

    print("\nДЕМОНСТРАЦИЯ ОПЕРАЦИЙ")

    print("1. Бинарное дерево поиска:")
    bst = BST.BST()
    for key in [5, 3, 7, 2, 4, 6, 8]:
        bst.insert(key)

    print(f"Высота: {bst.get_height()}")
    print(f"Прямой обход: {bst.preorder_traversal()}")
    print(f"Центрированный обход: {bst.inorder_traversal()}")
    print(f"Обратный обход: {bst.postorder_traversal()}")
    print(f"Обход в ширину: {bst.level_order_traversal()}")
    print(f"Минимум: {bst.find_min()}, Максимум: {bst.find_max()}")

    print("\n2. АВЛ-дерево:")
    avl = AVL.AVLTree()
    for key in [5, 3, 7, 2, 4, 6, 8]:
        avl.insert(key)

    print(f"Высота: {avl.get_height()}")
    print(f"Прямой обход: {avl.preorder_traversal()}")
    print(f"Центрированный обход: {avl.inorder_traversal()}")
    print(f"Обратный обход: {avl.postorder_traversal()}")
    print(f"Обход в ширину: {avl.level_order_traversal()}")

    print("\n3. Красно-черное дерево:")
    rb = RB.RedBlackTree()
    for key in [5, 3, 7, 2, 4, 6, 8]:
        rb.insert(key)

    print(f"Высота: {rb.get_height()}")
    print(f"Центрированный обход: {rb.inorder_traversal()}")
    print(f"обход: {rb.level_order_traversal()}")


if __name__ == "__main__":
    main()