# netlify-lfs-resize-url

This plugin provides a filter that allows the user to generate [Netlify Image Transformation](https://www.netlify.com/docs/image-transformation/) resize URL parameters when working with [Netlify Large Media](https://www.netlify.com/docs/large-media/).

## Installation

You can install this plugin by running the following command in your project's directory:

    lektor plugins add netlify-lfs-resize-url

## Usage

The `nf_resize` filter works in conjunction with the `url` filter as follows:

    {% for image in this.attachments.images %}
        <img src="{{ image|url|nf_resize(w=720) }}">
    {% endfor %}

The above will return the following:

`<img src="/images/example.png?nf_resize=fit&w=720">`

### Arguments

Arguments correspond to [Netlify transformation parameters](https://www.netlify.com/docs/image-transformation/#parameters-for-transformation).

| Argument | Accepts | Default |
|-------------|--------------------|---------|
| `nf_resize` | 'fit', 'smartcrop' | 'fit' |
| `h` | Positive integers | `null` |
| `w` | Positive integers | `null` |