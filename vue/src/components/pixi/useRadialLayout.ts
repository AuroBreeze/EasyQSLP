export type Vec2 = { x: number; y: number }
export type LayoutNode<T = any> = { id: string; label: string; data?: T; children?: LayoutNode<T>[] }

export function radialLayout<T = any>(
  nodes: LayoutNode<T>[],
  center: Vec2,
  radius: number,
  startAngle = -Math.PI / 2,
): (LayoutNode<T> & Vec2)[] {
  const n = Math.max(1, nodes.length)
  const step = (Math.PI * 2) / n
  return nodes.map((node, i) => {
    const angle = startAngle + i * step
    return {
      ...node,
      x: center.x + Math.cos(angle) * radius,
      y: center.y + Math.sin(angle) * radius,
    }
  })
}
