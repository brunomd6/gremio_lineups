FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    latexmk \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

RUN pip install svgwrite pyyaml pylatex

CMD ["python", "scripts/generator.py"]
