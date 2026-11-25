import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { 
  ReactFlow, 
  Controls, 
  Background, 
  useNodesState, 
  useEdgesState,
  Handle,
  Position,
  NodeProps,
  Edge,
  Node,
  MarkerType
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { hierarchy, tree } from 'd3-hierarchy';
import { Button } from "@/components/ui/button";
import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from "@/components/ui/breadcrumb";
import { DropdownMenu, DropdownMenuContent, DropdownMenuGroup, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from "@/components/ui/alert-dialog";
import { 
  RefreshCw, 
  Trash2, 
  MoreVertical, 
  ChevronRight, 
  ChevronDown, 
  XCircle, 
  Download, 
  Layers, 
  Minimize2, 
  Maximize2,
  Info,
  X,
  Sparkles
} from 'lucide-react';
import { MindMap, MindMapNode as MindMapNodeType } from '../types';
import { downloadMindMapPDF } from "@/lib/pdfExport";

interface MindMapStudioViewProps {
  notebookId: string;
  sourceIds: string[];
  notebookName: string;
  onBackToStudio: () => void;
}

// ---------------------------------------------------------------------------
// Contrasting Color Palette per Branch Theme
// ---------------------------------------------------------------------------
interface BranchTheme {
  name: string;
  border: string;
  bgLight: string;
  headerBg: string;
  headerText: string;
  accent: string;
  badge: string;
  text: string;
}

const BRANCH_THEMES: BranchTheme[] = [
  {
    name: "indigo",
    border: "border-indigo-500/80 dark:border-indigo-400",
    bgLight: "bg-indigo-50/70 dark:bg-indigo-950/30",
    headerBg: "bg-indigo-500",
    headerText: "text-white",
    accent: "#6366f1",
    badge: "bg-indigo-100 text-indigo-800 dark:bg-indigo-900/60 dark:text-indigo-300",
    text: "text-indigo-950 dark:text-indigo-100",
  },
  {
    name: "emerald",
    border: "border-emerald-500/80 dark:border-emerald-400",
    bgLight: "bg-emerald-50/70 dark:bg-emerald-950/30",
    headerBg: "bg-emerald-500",
    headerText: "text-white",
    accent: "#10b981",
    badge: "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 dark:text-emerald-300",
    text: "text-emerald-950 dark:text-emerald-100",
  },
  {
    name: "amber",
    border: "border-amber-500/80 dark:border-amber-400",
    bgLight: "bg-amber-50/70 dark:bg-amber-950/30",
    headerBg: "bg-amber-500",
    headerText: "text-white",
    accent: "#f59e0b",
    badge: "bg-amber-100 text-amber-800 dark:bg-amber-900/60 dark:text-amber-300",
    text: "text-amber-950 dark:text-amber-100",
  },
  {
    name: "purple",
    border: "border-purple-500/80 dark:border-purple-400",
    bgLight: "bg-purple-50/70 dark:bg-purple-950/30",
    headerBg: "bg-purple-500",
    headerText: "text-white",
    accent: "#a855f7",
    badge: "bg-purple-100 text-purple-800 dark:bg-purple-900/60 dark:text-purple-300",
    text: "text-purple-950 dark:text-purple-100",
  },
  {
    name: "rose",
    border: "border-rose-500/80 dark:border-rose-400",
    bgLight: "bg-rose-50/70 dark:bg-rose-950/30",
    headerBg: "bg-rose-500",
    headerText: "text-white",
    accent: "#f43f5e",
    badge: "bg-rose-100 text-rose-800 dark:bg-rose-900/60 dark:text-rose-300",
    text: "text-rose-950 dark:text-rose-100",
  },
  {
    name: "cyan",
    border: "border-cyan-500/80 dark:border-cyan-400",
    bgLight: "bg-cyan-50/70 dark:bg-cyan-950/30",
    headerBg: "bg-cyan-500",
    headerText: "text-white",
    accent: "#06b6d4",
    badge: "bg-cyan-100 text-cyan-800 dark:bg-cyan-900/60 dark:text-cyan-300",
    text: "text-cyan-950 dark:text-cyan-100",
  },
];

// ---------------------------------------------------------------------------
// Custom Node Component with Layer & Depth Specialization
// ---------------------------------------------------------------------------
const CustomNode = ({ data, isConnectable }: NodeProps) => {
  const { 
    id,
    label, 
    summary, 
    depth, 
    branchIndex, 
    childCount, 
    hasChildren, 
    isExpanded, 
    isRoot, 
    isSelected,
    onToggle, 
    onSelect 
  } = data as any;

  const theme: BranchTheme | undefined = 
    branchIndex >= 0 ? BRANCH_THEMES[branchIndex % BRANCH_THEMES.length] : undefined;

  // Depth 0: Core Knowledge Hub
  if (isRoot) {
    return (
      <div 
        onClick={onSelect}
        className={`relative min-w-[220px] max-w-[260px] rounded-xl border-2 border-indigo-400/90 bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white p-3.5 shadow-xl transition-all duration-200 cursor-pointer ${
          isSelected ? 'ring-2 ring-indigo-400 ring-offset-2 ring-offset-background' : ''
        }`}
      >
        <Handle type="target" position={Position.Left} style={{ visibility: 'hidden' }} isConnectable={isConnectable} />
        
        <div className="flex items-center gap-1.5 mb-1.5">
          <Sparkles className="w-3.5 h-3.5 text-indigo-300 animate-pulse" />
          <span className="text-[10px] uppercase font-bold tracking-wider text-indigo-300 bg-indigo-500/30 px-2 py-0.5 rounded-full">
            Core Knowledge Hub
          </span>
        </div>

        <div className="font-bold text-sm text-white leading-snug break-words">
          {label}
        </div>

        {summary && (
          <div className="text-[11px] text-indigo-200/70 mt-1 line-clamp-1 italic">
            {summary}
          </div>
        )}

        <div className="flex items-center justify-between mt-2.5 pt-2 border-t border-indigo-800/60 text-[11px] text-indigo-200/80">
          <span className="font-medium">{childCount} Major Branches</span>
          {hasChildren && (
            <button 
              onClick={(e) => { e.stopPropagation(); onToggle(); }}
              className="flex items-center justify-center w-5 h-5 rounded hover:bg-indigo-800/60 text-white transition-colors"
              title={isExpanded ? "Collapse branches" : "Expand branches"}
            >
              {isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
            </button>
          )}
        </div>

        <Handle type="source" position={Position.Right} style={{ visibility: 'hidden' }} isConnectable={isConnectable} />
      </div>
    );
  }

  // Depth 1: Major Themes (Distinct High-Contrast Header Card)
  if (depth === 1 && theme) {
    return (
      <div 
        onClick={onSelect}
        className={`relative min-w-[210px] max-w-[250px] rounded-xl border-2 ${theme.border} bg-card text-card-foreground p-3 shadow-md hover:shadow-lg transition-all duration-200 cursor-pointer ${
          isSelected ? 'ring-2 ring-primary ring-offset-2 ring-offset-background' : ''
        }`}
      >
        <Handle type="target" position={Position.Left} style={{ visibility: 'hidden' }} isConnectable={isConnectable} />
        
        <div className="flex items-center justify-between gap-1 mb-1.5">
          <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-md ${theme.badge}`}>
            Theme {branchIndex + 1}
          </span>
          {childCount > 0 && (
            <span className="text-[10px] text-muted-foreground font-medium">
              {childCount} topics
            </span>
          )}
        </div>

        <div className="font-bold text-sm text-foreground leading-snug break-words">
          {label}
        </div>

        {summary && (
          <div className="text-[11px] text-muted-foreground mt-1 line-clamp-2 leading-relaxed">
            {summary}
          </div>
        )}

        {hasChildren && (
          <div className="flex items-center justify-between mt-2 pt-1.5 border-t border-border/50 text-[11px]">
            <span className="text-[10px] text-muted-foreground">Click to toggle layer</span>
            <button 
              onClick={(e) => { e.stopPropagation(); onToggle(); }}
              className={`flex items-center justify-center w-5 h-5 rounded ${theme.badge} hover:opacity-80 transition-opacity`}
              title={isExpanded ? "Collapse subtopics" : "Expand subtopics"}
            >
              {isExpanded ? <ChevronDown size={13} /> : <ChevronRight size={13} />}
            </button>
          </div>
        )}

        <Handle type="source" position={Position.Right} style={{ visibility: 'hidden' }} isConnectable={isConnectable} />
      </div>
    );
  }

  // Depth 2 & 3+: Subtopics and Detailed Concepts
  const accentColor = theme?.accent || '#6366f1';
  return (
    <div 
      onClick={onSelect}
      style={{ borderLeftColor: accentColor }}
      className={`relative min-w-[190px] max-w-[230px] rounded-lg border border-border border-l-4 bg-card/95 text-card-foreground p-2.5 shadow-sm hover:shadow-md transition-all duration-200 cursor-pointer ${
        isSelected ? 'ring-2 ring-primary ring-offset-2 ring-offset-background' : ''
      }`}
    >
      <Handle type="target" position={Position.Left} style={{ visibility: 'hidden' }} isConnectable={isConnectable} />
      
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          <div className="font-semibold text-xs text-foreground leading-tight break-words">
            {label}
          </div>
          {summary && (
            <div className="text-[10px] text-muted-foreground mt-1 line-clamp-1 leading-snug">
              {summary}
            </div>
          )}
        </div>

        {hasChildren && (
          <button 
            onClick={(e) => { e.stopPropagation(); onToggle(); }}
            className="shrink-0 flex items-center justify-center w-4 h-4 rounded bg-muted hover:bg-muted/80 text-muted-foreground transition-colors"
            title={isExpanded ? "Collapse" : "Expand"}
          >
            {isExpanded ? <ChevronDown size={12} /> : <ChevronRight size={12} />}
          </button>
        )}
      </div>

      {childCount > 0 && !isExpanded && (
        <div className="mt-1.5 flex items-center gap-1">
          <span className="text-[9px] font-medium px-1.5 py-0.2 rounded bg-muted text-muted-foreground">
            +{childCount} more
          </span>
        </div>
      )}

      <Handle type="source" position={Position.Right} style={{ visibility: 'hidden' }} isConnectable={isConnectable} />
    </div>
  );
};

const nodeTypes = { custom: CustomNode };

// ---------------------------------------------------------------------------
// Main MindMapStudioView Component
// ---------------------------------------------------------------------------
export const MindMapStudioView: React.FC<MindMapStudioViewProps> = ({
  notebookId,
  sourceIds,
  notebookName,
  onBackToStudio
}) => {
  const [mindMapData, setMindMapData] = useState<MindMap | null>(null);
  const [viewState, setViewState] = useState<"loading" | "ready" | "error">("loading");
  const [errorMessage, setErrorMessage] = useState("");
  const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set());
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  
  const [showRegenerateDialog, setShowRegenerateDialog] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);

  // Collect all node IDs for Expand All
  const allNodeIds = useMemo(() => {
    if (!mindMapData || !mindMapData.root) return [];
    const ids: string[] = [];
    const traverse = (n: MindMapNodeType) => {
      ids.push(n.id);
      (n.children || []).forEach(traverse);
    };
    traverse(mindMapData.root);
    return ids;
  }, [mindMapData]);

  const areAllExpanded = useMemo(() => {
    if (allNodeIds.length === 0) return false;
    return allNodeIds.every(id => expandedNodes.has(id));
  }, [allNodeIds, expandedNodes]);

  const toggleExpandAll = () => {
    if (areAllExpanded) {
      // Collapse back to root only
      if (mindMapData?.root) {
        setExpandedNodes(new Set([mindMapData.root.id]));
      }
    } else {
      // Expand all nodes
      setExpandedNodes(new Set(allNodeIds));
    }
  };

  const fetchMindMap = useCallback(async (regenerate = false) => {
    setViewState("loading");
    setErrorMessage("");
    try {
      const res = await fetch(`/api/notebooks/${notebookId}/mindmap`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sourceIds, regenerate }),
      });

      if (!res.ok) {
        let errText = "Failed to generate mind map";
        try {
          const clone = res.clone();
          const data = await clone.json();
          errText = data.error || errText;
        } catch {
          const text = await res.text();
          if (text) errText = text;
        }
        throw new Error(errText);
      }

      const data = await res.json();
      setMindMapData(data.mindMap);
      
      // Auto-expand root AND its immediate children (Depth 0 & 1)
      const initialExpanded = new Set<string>();
      if (data.mindMap.root) {
        initialExpanded.add(data.mindMap.root.id);
        for (const child of data.mindMap.root.children || []) {
          initialExpanded.add(child.id);
        }
      }
      setExpandedNodes(initialExpanded);
      setViewState("ready");
    } catch (err) {
      setErrorMessage((err as Error).message);
      setViewState("error");
    }
  }, [notebookId, sourceIds]);

  useEffect(() => {
    fetchMindMap();
  }, [fetchMindMap]);

  const handleToggleNode = useCallback((nodeId: string) => {
    setExpandedNodes(prev => {
      const next = new Set(prev);
      if (next.has(nodeId)) {
        next.delete(nodeId);
      } else {
        next.add(nodeId);
      }
      return next;
    });
  }, []);

  // Compute Layout whenever data or expanded state changes
  useEffect(() => {
    if (!mindMapData || !mindMapData.root) return;

    // Filter tree based on expanded nodes
    const filterTree = (node: MindMapNodeType): MindMapNodeType => {
      if (expandedNodes.has(node.id) && node.children && node.children.length > 0) {
        return { ...node, children: node.children.map(filterTree) };
      }
      return { ...node, children: [] };
    };

    const visibleTree = filterTree(mindMapData.root);
    
    // Create D3 hierarchy
    const root = hierarchy(visibleTree);
    
    // Compute tree layout: nodeSize([verticalGap, horizontalGap])
    const nodeWidth = 240;
    const nodeHeight = 85;
    const treeLayout = tree<MindMapNodeType>().nodeSize([nodeHeight * 1.5, nodeWidth * 1.4]);
    treeLayout(root);

    const newNodes: Node[] = [];
    const newEdges: Edge[] = [];

    // Helper to find original node for actual child count
    const findOrigNode = (n: MindMapNodeType, id: string): MindMapNodeType | null => {
      if (n.id === id) return n;
      for (const child of n.children || []) {
        const found = findOrigNode(child, id);
        if (found) return found;
      }
      return null;
    };

    // Helper to determine branch index (which child of root this node belongs to)
    const getBranchIndex = (d3Node: any): number => {
      if (d3Node.depth === 0) return -1;
      let curr = d3Node;
      while (curr.parent && curr.parent.depth !== 0) {
        curr = curr.parent;
      }
      if (curr.parent && curr.parent.depth === 0) {
        const rootChildren = curr.parent.children || [];
        return rootChildren.indexOf(curr);
      }
      return 0;
    };

    root.each((node) => {
      const origNode = findOrigNode(mindMapData.root, node.data.id);
      const actualChildren = origNode?.children || [];
      const hasChildren = actualChildren.length > 0;
      const branchIdx = getBranchIndex(node);
      const branchTheme = branchIdx >= 0 ? BRANCH_THEMES[branchIdx % BRANCH_THEMES.length] : undefined;

      newNodes.push({
        id: node.data.id,
        type: 'custom',
        position: { x: node.y || 0, y: node.x || 0 },
        data: { 
          id: node.data.id,
          label: node.data.label,
          summary: origNode?.summary || node.data.summary,
          depth: node.depth,
          branchIndex: branchIdx,
          childCount: actualChildren.length,
          hasChildren: hasChildren,
          isExpanded: expandedNodes.has(node.data.id),
          isRoot: node.depth === 0,
          isSelected: selectedNodeId === node.data.id,
          onToggle: () => handleToggleNode(node.data.id),
          onSelect: () => setSelectedNodeId(node.data.id),
        },
      });

      if (node.parent) {
        const edgeColor = branchTheme ? branchTheme.accent : '#6366f1';
        newEdges.push({
          id: `e-${node.parent.data.id}-${node.data.id}`,
          source: node.parent.data.id,
          target: node.data.id,
          type: 'smoothstep',
          animated: false,
          style: { stroke: edgeColor, strokeWidth: node.depth === 1 ? 2.2 : 1.6 },
          markerEnd: {
            type: MarkerType.ArrowClosed,
            color: edgeColor,
          },
        });
      }
    });

    setNodes(newNodes);
    setEdges(newEdges);
  }, [mindMapData, expandedNodes, selectedNodeId, setNodes, setEdges, handleToggleNode]);

  // Selected node details
  const selectedNodeInfo = useMemo(() => {
    if (!selectedNodeId || !mindMapData) return null;
    const findNode = (n: MindMapNodeType, depth = 0, bIdx = -1): any | null => {
      if (n.id === selectedNodeId) {
        return { node: n, depth, branchIndex: bIdx };
      }
      for (let i = 0; i < (n.children || []).length; i++) {
        const childBIdx = depth === 0 ? i : bIdx;
        const found = findNode(n.children[i], depth + 1, childBIdx);
        if (found) return found;
      }
      return null;
    };
    return findNode(mindMapData.root);
  }, [selectedNodeId, mindMapData]);

  const handleRegenerate = () => {
    setShowRegenerateDialog(false);
    fetchMindMap(true);
  };

  const handleDelete = async () => {
    setShowDeleteDialog(false);
    if (mindMapData) {
      try {
        await fetch(`/api/notebooks/${notebookId}/mindmap/${mindMapData.id}`, { method: "DELETE" });
      } catch {
        // silent
      }
    }
    onBackToStudio();
  };

  return (
    <div className="flex flex-col h-full bg-muted/20">
      {/* Header */}
      <header className="flex items-center justify-between p-3.5 border-b border-border bg-background shrink-0 z-10">
        <Breadcrumb>
          <BreadcrumbList>
            <BreadcrumbItem>
              <BreadcrumbLink onClick={onBackToStudio} className="text-muted-foreground hover:text-foreground cursor-pointer">
                Studio
              </BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem>
              <BreadcrumbPage>Mind Map</BreadcrumbPage>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>

        {viewState === "ready" && mindMapData && (
          <div className="flex items-center gap-2">
            {/* Expand / Collapse All Toggle */}
            <Button
              variant="outline"
              size="sm"
              onClick={toggleExpandAll}
              className="h-8 text-xs font-medium gap-1.5"
              title={areAllExpanded ? "Collapse down to root" : "Expand all branches and subtopics"}
            >
              {areAllExpanded ? (
                <>
                  <Minimize2 className="w-3.5 h-3.5" />
                  Collapse All
                </>
              ) : (
                <>
                  <Maximize2 className="w-3.5 h-3.5" />
                  Expand All
                </>
              )}
            </Button>

            {/* Prominent Download PDF Button */}
            <Button
              variant="outline"
              size="sm"
              onClick={() => downloadMindMapPDF(mindMapData, notebookName)}
              className="h-8 text-xs font-medium gap-1.5 border-primary/40 bg-primary/5 hover:bg-primary/10 text-foreground transition-colors shadow-sm"
              title="Download formatted Mind Map PDF"
            >
              <Download className="h-3.5 w-3.5 text-primary" />
              Download PDF
            </Button>

            <DropdownMenu>
              <DropdownMenuTrigger>
                <Button variant="ghost" size="icon" className="size-8">
                  <MoreVertical className="w-4 h-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuGroup>
                  <DropdownMenuItem onClick={() => downloadMindMapPDF(mindMapData, notebookName)}>
                    <Download data-icon="inline-start" />
                    Export as PDF
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => setShowRegenerateDialog(true)}>
                    <RefreshCw data-icon="inline-start" />
                    Regenerate
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => setShowDeleteDialog(true)} className="text-destructive focus:text-destructive">
                    <Trash2 data-icon="inline-start" />
                    Delete mind map
                  </DropdownMenuItem>
                </DropdownMenuGroup>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        )}
      </header>

      {/* Main Content Area */}
      <div className="flex-1 w-full relative overflow-hidden">
        {viewState === "loading" && (
          <div className="absolute inset-0 flex flex-col items-center justify-center space-y-6 text-center z-20 bg-background/50 backdrop-blur-sm">
            <RefreshCw className="size-10 animate-spin text-primary" />
            <div className="space-y-2">
              <h3 className="text-xl font-medium">Generating mind map...</h3>
              <p className="text-muted-foreground">Synthesizing deep concepts from {sourceIds.length} source(s)</p>
            </div>
          </div>
        )}

        {viewState === "error" && (
          <div className="absolute inset-0 flex flex-col items-center justify-center space-y-6 text-center z-20 bg-background">
            <div className="rounded-full bg-destructive/10 p-4">
              <XCircle className="size-10 text-destructive" />
            </div>
            <div className="space-y-2 max-w-md">
              <h3 className="text-xl font-medium">Generation Failed</h3>
              <p className="text-muted-foreground">{errorMessage}</p>
            </div>
            <div className="flex gap-4">
              <Button variant="outline" onClick={onBackToStudio}>
                Back to Studio
              </Button>
              <Button onClick={() => fetchMindMap(true)}>Retry</Button>
            </div>
          </div>
        )}

        {viewState === "ready" && (
          <>
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              nodeTypes={nodeTypes}
              fitView
              fitViewOptions={{ padding: 0.15 }}
              minZoom={0.15}
              maxZoom={2.2}
              proOptions={{ hideAttribution: true }}
            >
              <Background color="hsl(var(--muted-foreground))" gap={18} />
              <Controls />
            </ReactFlow>

            {/* Floating Concept Inspector Drawer */}
            {selectedNodeInfo && (
              <div className="absolute bottom-5 right-5 w-80 max-w-[calc(100vw-40px)] bg-card border border-border shadow-2xl rounded-xl p-4 z-30 animate-in fade-in slide-in-from-bottom-2 duration-200">
                <div className="flex items-start justify-between gap-2 mb-2 pb-2 border-b border-border">
                  <div>
                    <span className="text-[10px] uppercase font-bold tracking-wider text-muted-foreground">
                      {selectedNodeInfo.depth === 0 
                        ? "Core Topic" 
                        : selectedNodeInfo.depth === 1 
                        ? `Theme ${selectedNodeInfo.branchIndex + 1}` 
                        : `Subtopic Layer ${selectedNodeInfo.depth}`}
                    </span>
                    <h4 className="text-sm font-bold text-foreground leading-snug">
                      {selectedNodeInfo.node.label}
                    </h4>
                  </div>
                  <button 
                    onClick={() => setSelectedNodeId(null)}
                    className="p-1 rounded-md text-muted-foreground hover:bg-muted hover:text-foreground"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>

                <div className="text-xs text-muted-foreground leading-relaxed max-h-40 overflow-y-auto mb-3">
                  {selectedNodeInfo.node.summary || "No specific summary available for this concept."}
                </div>

                <div className="flex items-center justify-between text-[11px] pt-2 border-t border-border">
                  <span className="text-muted-foreground">
                    {(selectedNodeInfo.node.children || []).length} direct subtopics
                  </span>
                  {(selectedNodeInfo.node.children || []).length > 0 && (
                    <Button 
                      size="sm" 
                      variant="secondary"
                      className="h-7 text-xs px-2.5"
                      onClick={() => handleToggleNode(selectedNodeInfo.node.id)}
                    >
                      {expandedNodes.has(selectedNodeInfo.node.id) ? "Collapse Layer" : "Expand Layer"}
                    </Button>
                  )}
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* Dialogs */}
      <AlertDialog open={showRegenerateDialog} onOpenChange={setShowRegenerateDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Regenerate mind map?</AlertDialogTitle>
            <AlertDialogDescription>
              This will create a new multi-layered mind map and replace the current one.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={handleRegenerate}>Regenerate</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      <AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete this mind map?</AlertDialogTitle>
            <AlertDialogDescription>
              This mind map will be permanently deleted.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};