import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight } from 'lucide-react';

interface PaginationControlProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  isLoading: boolean;
}

export default function paginationControl({ 
  currentPage, 
  totalPages, 
  onPageChange, 
  isLoading 
}: PaginationControlProps) {
  if (totalPages <= 1) return null;

  return (
    <div className="flex items-center justify-center gap-4 mt-8 p-4">
      <Button
        variant="ghost"
        size="icon"
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1 || isLoading}
        className="text-gray-600 hover:text-gray-800 cursor-pointer"
      >
        <ChevronLeft strokeWidth={4}  className="!w-6 !h-6" />
      </Button>
      
      <span className="text-sm font-medium text-gray-600">
        Página {currentPage} de {totalPages}
      </span>

      <Button
        variant="ghost"
        size="icon"
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages || isLoading}
        className="text-gray-600 hover:text-black cursor-pointer"
      >
        <ChevronRight strokeWidth={4}  className="!w-6 !h-6"/>
      </Button>
    </div>
  );
}