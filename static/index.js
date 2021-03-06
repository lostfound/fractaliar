// Generated by CoffeeScript 1.6.2
(function() {
  var Layout, down_xy, mouse_is_down, onmousedown, onmouseup, parse_transforms, rotate, set_events, set_stroke, stroke, t, th, trfm, tt,
    _this = this;

  th = this;

  set_events = function() {
    $('.fractal_select').change(function() {
      var fractal_node, n,
        _this = this;

      n = $(this).find(':selected')[0].value;
      fractal_node = $(this).parent().parent().find('.base_fractal')[0];
      return $.get("fractal", {
        n: n
      }, function(data) {
        return $(fractal_node).html(data);
      });
    });
    $('#Plus').click(function() {
      var clone, fr, me, v;

      me = $(this).parent().parent();
      fr = me.parent().find('.base_fractal')[0];
      clone = $(fr).parent().clone();
      clone.appendTo(me.parent());
      v = $('.fractal_select', $(fr).parent())[0].value;
      $('.fractal_select', clone)[0].value = v;
      me.clone().appendTo(me.parent());
      $(this).parent().parent().attr('class', 'plus');
      $(this).parent().parent().html('+');
      return set_events();
    });
    $('#RM').click(function() {
      var flst, l, plst;

      flst = $('.fractal');
      if (flst.length === 1) {
        return;
      }
      l = flst.length - 1;
      $(flst[l]).remove();
      plst = $('.plus');
      return $(plst[plst.length - 1]).remove();
    });
    return $('#EQ').click(function() {
      var fractal, fractals, params, shape, _i, _len, _ref,
        _this = this;

      shape = $('#shape_select').find(':selected')[0].value;
      fractals = null;
      _ref = $('.fractal_select');
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        fractal = _ref[_i];
        if (fractals) {
          fractals += 'x' + $(fractal).find(':selected')[0].value;
        } else {
          fractals = $(fractal).find(':selected')[0].value;
        }
      }
      params = {
        shape: shape,
        fractals: fractals
      };
      if (th.fractal_file) {
        params.layout = th.lno;
        params.filename = th.fractal_file;
      }
      return $.get("gen", params, function(url) {
        th.fractal_file = url;
        $('#link').html('<a href="' + url + '">Fractal here</a>');
        return $.get(url, {}, function(data) {
          var l, _j, _len1;

          $('#result').html((new XMLSerializer()).serializeToString(data));
          if (th.lno === void 0) {
            th.layouts.push(new Layout(0));
            th.lno = 0;
          }
          for (_j = 0, _len1 = layouts.length; _j < _len1; _j++) {
            l = layouts[_j];
            l.set_transforms();
            l.set_color(null);
          }
          $('#result').children()[0].addEventListener('mousedown', onmousedown, false);
          return $('#result').children()[0].addEventListener('mouseup', onmouseup, false);
        });
      });
    });
  };

  mouse_is_down = false;

  down_xy = [0, 0];

  onmousedown = function(e) {
    down_xy = [e.pageX, e.pageY];
    return mouse_is_down = true;
  };

  onmouseup = function(e) {
    var dlt;

    if (!mouse_is_down) {
      return;
    }
    dlt = [e.pageX - down_xy[0], e.pageY - down_xy[1]];
    return layout().dragnmove(dlt);
  };

  Layout = (function() {
    function Layout(nu) {
      this.nu = nu;
      this.xy = [100, 100];
      this.step = 3;
      this.scale_step = .3;
      this.scale = 3;
      this.stroke = 4;
      this.rotate = 0;
      this.color = 'black';
      this.set_transforms = function() {
        return $('#ff' + this.nu).attr('transform', 'translate(' + this.xy[0] + ',' + this.xy[1] + ') scale(' + this.scale + ') rotate(' + this.rotate + ')');
      };
      this.set_stroke = function(stroke) {
        this.stroke = stroke;
        return $('#ff' + this.nu).attr('stroke-width', this.stroke);
      };
      this.inc_rotate = function(dlt) {
        this.rotate -= dlt;
        return this.set_transforms();
      };
      this.dragnmove = function(dlt) {
        this.xy[0] += dlt[0];
        this.xy[1] += dlt[1];
        return this.set_transforms();
      };
      this.up = function() {
        this.xy[1] -= this.step;
        return this.set_transforms();
      };
      this.down = function() {
        this.xy[1] += this.step;
        return this.set_transforms();
      };
      this.left = function() {
        this.xy[0] -= this.step;
        return this.set_transforms();
      };
      this.right = function() {
        this.xy[0] += this.step;
        return this.set_transforms();
      };
      this.zoomin = function() {
        this.scale += .3;
        return this.set_transforms();
      };
      this.zoomout = function() {
        this.scale -= .3;
        return this.set_transforms();
      };
      this.set_color = function(color) {
        if (color !== null) {
          this.color = color;
        }
        return $('#ff' + this.nu).attr('stroke', this.color);
      };
      return this;
    }

    return Layout;

  })();

  trfm = null;

  stroke = null;

  rotate = 0;

  t = new Layout(0);

  tt = new Layout(1);

  this.fractal_file = void 0;

  this.lno = void 0;

  this.layouts = [];

  this.layout = function() {
    return _this.layouts[_this.lno];
  };

  parse_transforms = function() {
    var scale, ts, x, y;

    t = $('#ff0').attr('transform');
    ts = t.split(',');
    x = parseInt(ts[0].split('(')[1]);
    y = parseInt(ts[1].split(')')[0]);
    scale = parseFloat(t.split('(')[2].split(')')[0]);
    return [x, y, scale];
  };

  set_stroke = function(w) {
    $('#ff0').attr('stroke-width', w);
    return stroke = w;
  };

  $(document).ready(function() {
    var fractal_node, n;

    $('#picker').farbtastic(function(cl) {
      var color;

      color = cl;
      return th.layout().set_color(cl);
    });
    n = $('#shape_select')[0].value;
    $.get("shape", {
      n: n
    }, function(data) {
      return $('#base_shape').html(data);
    });
    n = $('.fractal_select').find(':selected')[0].value;
    fractal_node = $('.fractal_select').parent().parent().find('.base_fractal')[0];
    $.get("fractal", {
      n: n
    }, function(data) {
      return $(fractal_node).html(data);
    });
    $('#shape_select').change(function() {
      var _this = this;

      n = $(this).find(':selected')[0].value;
      return $.get("shape", {
        n: n
      }, function(data) {
        return $('#base_shape').html(data);
      });
    });
    $('#Up').click(function() {
      return layout().up();
    });
    $('#Down').click(function() {
      return layout().down();
    });
    $('#Left').click(function() {
      return layout().left();
    });
    $('#Right').click(function() {
      return layout().right();
    });
    $('#Zoomin').click(function() {
      return layout().zoomin();
    });
    $('#Zoomout').click(function() {
      return layout().zoomout();
    });
    $('#stroke').change(function() {
      return layout().set_stroke($(this).find(':selected')[0].value);
    });
    $('#Rotate').click(function() {
      return layout().inc_rotate(10);
    });
    $('#deRotate').click(function() {
      return layout().inc_rotate(-10);
    });
    $('#Layout').change(function() {
      var lv;

      lv = $(this).find(':selected')[0].value;
      if (lv === 'NEW') {
        if (th.lno === void 0) {
          return;
        }
        th.lno += 1;
        th.layouts.push(new Layout(th.lno));
        $(this).find(':selected')[0].value = th.lno;
        $($(this).find(':selected')[0]).html(th.lno);
        return $(this).append($('<option value="NEW">New</option>'));
      } else {
        return th.lno = parseInt(lv);
      }
    });
    return set_events();
  });

}).call(this);
