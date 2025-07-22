import matplotlib.pyplot as plt
import random
import streamlit as st

# 3x3 grid coordinates
dot_coords = {
    0: (0, 2), 1: (1, 2), 2: (2, 2),
    3: (0, 1), 4: (1, 1), 5: (2, 1),
    6: (0, 0), 7: (1, 0), 8: (2, 0),
}

# Pairs that require an auto-middle dot
auto_middle = {
    frozenset({0, 8}): 4, 
    frozenset({2, 6}): 4, 
    frozenset({1, 7}): 4, 
    frozenset({3, 5}): 4, 
    frozenset({0, 2}): 1, 
    frozenset({6, 8}): 7, 
    frozenset({0, 6}): 3, 
    frozenset({2, 8}): 5
}


def insert_auto_middle(a, b, used):
    sequence = []
    mid = auto_middle.get(frozenset({a, b}))
    if mid is not None and mid not in used:
        sequence.append(mid)
    sequence.append(b)
    return sequence


def generate_symbol(start_seq, end_seq, length):
    while True:
        # Random start if it was not given
        if not start_seq:
            real_starts = []
            for n in [0,1,2,3,4,5,6,7,8]:
                if n not in end_seq:
                    real_starts.append(n)
            start_seq = [random.choice(real_starts)]

        path = start_seq[:]
        used = set(path)        

        def get_middle_candidates():
            candidates = [i for i in range(9) if i not in used and i not in end_seq]
            random.shuffle(candidates)
            return candidates

        # Generating the middle
        while True:
            remaining_slots = length - len(path) - len(end_seq)
            last = path[-1]
            added = False
            for candidate in get_middle_candidates():
                inserted = insert_auto_middle(last, candidate, used)
                if len(inserted) <= remaining_slots:
                    for dot in inserted:
                        if dot not in used:
                            path.append(dot)
                            used.add(dot)
                    added = True
                    break
            if not added:
                break

        # Adding end_seq dot if requested
        if end_seq:
            for dot in end_seq:
                last = path[-1]
                sequence = insert_auto_middle(last, dot, used)
                path.extend(sequence)
                used.update(sequence)
            
        if len(path) != length:
            continue    # Retry when path is incorrect length - due to auto_middle in end_seq

        return path


# =================================================================

def plot_symbol(path):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim(-1, 3)
    ax.set_ylim(-1, 3)
    ax.axis('off')

    for i, (x, y) in dot_coords.items():
        ax.plot(x, y, 'o', color='black', markersize=16)
        ax.text(x, y, str(i), ha='center', va='center', color='white', fontsize=9, fontweight='bold')

    for i in range(len(path) - 1):
        x1, y1 = dot_coords[path[i]]
        x2, y2 = dot_coords[path[i + 1]]
        ax.plot([x1, x2], [y1, y2], color='#D86B6B', linewidth=4)

    for idx, dot in enumerate(path):
        x, y = dot_coords[dot]
        ax.text(x, y - 0.25, f"{idx + 1}", color='#5B0C0C', ha='center', va='top', fontsize=8)

    return fig

# =========================
# Streamlit UI
# =========================
st.set_page_config(page_title = "Lock Screen Symbol Generator")
st.title("Lock Screen Symbol Generator")

start_input = st.text_input("Start sequence (comma-separated)", value="")
end_input = st.text_input("End sequence (comma-separated)", value="")
length = st.slider("Length of symbol", 4, 9, 4)

try:
    start = [int(x.strip()) for x in start_input.split(',') if x.strip().isdigit()]
    end = [int(x.strip()) for x in end_input.split(',') if x.strip().isdigit()]

    if st.button("Generate Symbol"):
        if any(n not in range(9) for n in start + end):
            raise Exception("Sequences must consist of numbers from 0 to 8")
        if len(list(set(start) & set(end))) > 0:
            raise Exception("Starting and ending sequences cannot have shared elements")


        symbol = generate_symbol(start, end, length)
        fig = plot_symbol(symbol)
        st.pyplot(fig)

except Exception as e:
    st.error(f"Error: {e}")

st.markdown("Made by [a-jednak](https://github.com/a-jednak) on GitHub")
