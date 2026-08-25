import type { Block, ColumnsBlock } from "./types";

export function walkBlocks(blocks: Block[], visit: (block: Block, parent: ColumnsBlock | null, side: "left" | "right" | null) => void, parent: ColumnsBlock | null = null, side: "left" | "right" | null = null) {
  for (const block of blocks) {
    visit(block, parent, side);
    if (block.type === "columns") {
      walkBlocks(block.left, visit, block, "left");
      walkBlocks(block.right, visit, block, "right");
    }
  }
}

export function findBlock(blocks: Block[], id: string): Block | null {
  let found: Block | null = null;
  walkBlocks(blocks, (block) => {
    if (block.id === id) found = block;
  });
  return found;
}

export function updateBlock(blocks: Block[], id: string, patch: Partial<Block>): Block[] {
  return blocks.map((block) => {
    if (block.id === id) {
      return { ...block, ...patch, id: block.id, type: block.type } as Block;
    }
    if (block.type === "columns") {
      return {
        ...block,
        left: updateBlock(block.left, id, patch),
        right: updateBlock(block.right, id, patch),
      };
    }
    return block;
  });
}

export function removeBlock(blocks: Block[], id: string): Block[] {
  return blocks
    .filter((block) => block.id !== id)
    .map((block) => {
      if (block.type === "columns") {
        return {
          ...block,
          left: removeBlock(block.left, id),
          right: removeBlock(block.right, id),
        };
      }
      return block;
    });
}

export function insertAfter(blocks: Block[], afterId: string | null, next: Block): Block[] {
  if (!afterId) return [...blocks, next];

  const index = blocks.findIndex((block) => block.id === afterId);
  if (index >= 0) {
    const copy = [...blocks];
    copy.splice(index + 1, 0, next);
    return copy;
  }

  return blocks.map((block) => {
    if (block.type !== "columns") return block;
    if (block.left.some((child) => child.id === afterId) || findBlock(block.left, afterId)) {
      return { ...block, left: insertAfter(block.left, afterId, next) };
    }
    if (block.right.some((child) => child.id === afterId) || findBlock(block.right, afterId)) {
      return { ...block, right: insertAfter(block.right, afterId, next) };
    }
    return block;
  });
}

export function insertIntoColumn(blocks: Block[], columnId: string, side: "left" | "right", next: Block): Block[] {
  return blocks.map((block) => {
    if (block.id === columnId && block.type === "columns") {
      return { ...block, [side]: [...block[side], next] };
    }
    if (block.type === "columns") {
      return {
        ...block,
        left: insertIntoColumn(block.left, columnId, side, next),
        right: insertIntoColumn(block.right, columnId, side, next),
      };
    }
    return block;
  });
}

function moveInArray(list: Block[], id: string, direction: -1 | 1): Block[] | null {
  const index = list.findIndex((block) => block.id === id);
  if (index < 0) return null;
  const target = index + direction;
  if (target < 0 || target >= list.length) return list;
  const copy = [...list];
  const [item] = copy.splice(index, 1);
  copy.splice(target, 0, item);
  return copy;
}

export function moveBlock(blocks: Block[], id: string, direction: -1 | 1): Block[] {
  const moved = moveInArray(blocks, id, direction);
  if (moved) return moved;
  return blocks.map((block) => {
    if (block.type !== "columns") return block;
    const left = moveBlock(block.left, id, direction);
    const right = moveBlock(block.right, id, direction);
    return { ...block, left, right };
  });
}

export function duplicateBlock(blocks: Block[], id: string, clone: (block: Block) => Block): Block[] {
  const index = blocks.findIndex((block) => block.id === id);
  if (index >= 0) {
    const copy = [...blocks];
    copy.splice(index + 1, 0, clone(blocks[index]));
    return copy;
  }
  return blocks.map((block) => {
    if (block.type !== "columns") return block;
    return {
      ...block,
      left: duplicateBlock(block.left, id, clone),
      right: duplicateBlock(block.right, id, clone),
    };
  });
}

export function cloneTree(block: Block): Block {
  const id = `${block.id}_copy_${Math.random().toString(36).slice(2, 6)}`;
  if (block.type === "columns") {
    return {
      ...block,
      id,
      left: block.left.map(cloneTree),
      right: block.right.map(cloneTree),
    };
  }
  if (block.type === "list") {
    return { ...block, id, items: [...block.items] };
  }
  if (block.type === "quiz") {
    return { ...block, id, options: [...block.options] };
  }
  return { ...block, id };
}

export function reorder(blocks: Block[], fromId: string, toId: string): Block[] {
  if (fromId === toId) return blocks;
  const fromIndex = blocks.findIndex((block) => block.id === fromId);
  const toIndex = blocks.findIndex((block) => block.id === toId);
  if (fromIndex >= 0 && toIndex >= 0) {
    const copy = [...blocks];
    const [item] = copy.splice(fromIndex, 1);
    copy.splice(toIndex, 0, item);
    return copy;
  }
  return blocks.map((block) => {
    if (block.type !== "columns") return block;
    return {
      ...block,
      left: reorder(block.left, fromId, toId),
      right: reorder(block.right, fromId, toId),
    };
  });
}
