import schemdraw
import schemdraw.elements as elm

# 1. 建立一個繪圖畫布 (Drawing)
d = schemdraw.Drawing()

# 2. 加入元件 (Add elements)
# 加入電壓源 (SourceV)，標籤設為 'V'，位置在左側
V = d.add(elm.SourceV().label('V', loc='left'))

# 加入電阻 (Resistor)，標籤 'R'，畫完後向右延伸
R = d.add(elm.Resistor().label('R').right())

# 加入電容 (Capacitor)，標籤 'C'，畫完後向右延伸
C = d.add(elm.Capacitor().label('C').right())

# 加入電感 (Inductor)，標籤 'L'，畫完後向右延伸
L = d.add(elm.Inductor().label('L').right())

# 3. 加入接地符號 (Ground)
# 在電壓源的起始點 (V.start) 加一個接地
d.add(elm.Ground().at(V.start))

# 在電感的結束點 (L.end) 加一個接地
d.add(elm.Ground().at(L.end))

# 4. 顯示圖表
d.draw()