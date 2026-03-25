FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-luatex \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-latex-extra \
    latexmk \
    && rm -rf /var/lib/apt/lists/* \
    && luaotfload-tool -u \

# Set workdir
WORKDIR /app

RUN pip install svgwrite pyyaml pylatex requests

CMD ["python", "scripts/generator.py"]
