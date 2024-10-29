import random
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
import markdown2
import os

# Ejemplo de contenido de entradas Markdown en un directorio
ENTRIES_DIR = "encyclopedia/entries"

def index(request):
    """Página principal que lista todas las entradas disponibles."""
    entries = [entry.replace(".md", "") for entry in os.listdir(ENTRIES_DIR) if entry.endswith(".md")]
    return render(request, "encyclopedia/index.html", {"entries": entries})

def entry(request, title):
    """Muestra una entrada específica en formato HTML convertido desde Markdown."""
    file_path = os.path.join(ENTRIES_DIR, f"{title}.md")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            content = markdown2.markdown(file.read())
        return render(request, "encyclopedia/entry.html", {"title": title, "content": content})
    else:
        return render(request, "encyclopedia/error.html", {"message": "La entrada no existe."})

def search(request):
    """Busca entradas y muestra los resultados."""
    query = request.GET.get("q", "")
    entries = [entry.replace(".md", "") for entry in os.listdir(ENTRIES_DIR) if entry.endswith(".md")]
    results = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "encyclopedia/search.html", {"query": query, "results": results})

def random_entry(request):
    """Muestra una entrada aleatoria."""
    entries = [entry.replace(".md", "") for entry in os.listdir(ENTRIES_DIR) if entry.endswith(".md")]
    title = random.choice(entries)
    return redirect(reverse("entry", kwargs={"title": title}))

def create_entry(request):
    """Permite crear una nueva entrada."""
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        file_path = os.path.join(ENTRIES_DIR, f"{title}.md")
        
        if os.path.exists(file_path):
            return render(request, "encyclopedia/error.html", {"message": "La entrada ya existe."})
        
        with open(file_path, "w") as file:
            file.write(content)
        return redirect(reverse("entry", kwargs={"title": title}))
    
    return render(request, "encyclopedia/create.html")

def edit_entry(request, title):
    """Permite editar una entrada existente."""
    file_path = os.path.join(ENTRIES_DIR, f"{title}.md")
    
    if request.method == "POST":
        content = request.POST.get("content")
        with open(file_path, "w") as file:
            file.write(content)
        return redirect(reverse("entry", kwargs={"title": title}))
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            content = file.read()
        return render(request, "encyclopedia/edit.html", {"title": title, "content": content})
    
    return render(request, "encyclopedia/error.html", {"message": "La entrada no existe."})