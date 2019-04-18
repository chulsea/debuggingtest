from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Board, Comment
from .forms import BoardForm, CommentForm

# Create your views here.
def list(request):
    boards = Board.objects.order_by('-pk')
    ctx = {
        'boards': boards,
    }
    return render(request, 'boards/list.html', ctx)

def detail(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    ctx = {
        'board': board,
        'form': CommentForm(),
    }
    return render(request, 'boards/detail.html', ctx)

@login_required
def create(request):
    if not request.user.is_authenticated:
        return redirect('boards:list')
        
    if request.method == 'POST':
        board_form = BoardForm(request.POST)
        if board_form.is_valid():
            board = board_form.save(commit=False)
            board.user = request.user
            board.save()
            return redirect('boards:detail', board.id)
    else:
        board_form = BoardForm()
    ctx = {
        'board_form': board_form,
    }
    return render(request, 'boards/form.html', ctx)

@login_required
def edit(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.user != board.user:
        return redirect('board:detail', board_pk)
    if request.method == 'POST':
        board_update_form = BoardForm(request.POST, instance=board)
        if board_update_form.is_valid():
            board_update_form.save()
            return redirect('boards:detail', board_pk)
    else:
        board_update_form = BoardForm(instance=board)
    ctx = {
        'form': board_update_form,
    }
    return render(request, 'boards/form.html', ctx)

@require_POST
def delete(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    board.delete()
    return redirect('boards:list')

@login_required
@require_POST
def comment_create(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment_form.save()
    return redirect('boards:detail', board_pk)

@login_required
@require_POST
def comment_delete(request, board_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('boards:detail', board_pk)
