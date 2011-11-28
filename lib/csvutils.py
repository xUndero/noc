# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## CSV import/export utilities
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Python modules
import csv
import cStringIO
## Django modules
from django.db import models


# CSV import conflict resolution constants
IR_FAIL = 0  # Fail on first conflict
IR_SKIP = 1  # Skip conflicted records
IR_UPDATE = 2  # Overwrite conflicted records


def get_model_fields(model):
    # Detect fields
    fields = []
    for f in model._meta.fields:
        if f.name == "id":
            continue
        required = not f.null and f.default == models.fields.NOT_PROVIDED
        # Process references
        if f.rel:
            if isinstance(f.rel, models.fields.related.ManyToOneRel):
                # Foreign Key
                # Try to find unique key
                k = "id"
                for ff in f.rel.to._meta.fields:
                    if ff.name != "id" and ff.unique:
                        k = ff.name
                        break
                fields += [(f.name, required, f.rel.to, k)]
        else:
            fields += [(f.name, required, None, None)]
    return fields


def csv_export(model, queryset=None):
    """
    Export to CSV
    """
    io = cStringIO.StringIO()
    writer = csv.writer(io)
    fields = get_model_fields(model)
    # Write header
    writer.writerow([f[0] for f in fields])
    # Build queryset
    if queryset is None:
        queryset = model.objects.all()
        # Write rows
    for r in queryset:
        row = []
        # Format row
        for f, required, rel, rf in fields:
            v = getattr(r, f)
            if v is None:
                v = ""
            if rel is None or not v:
                row += [v]
            else:
                row += [getattr(v, rf)]
        row = [unicode(f).encode("utf-8") for f in row]
        writer.writerow(row)
        # Return result
    return io.getvalue()

IGNORED_REQUIRED = {
    "ip_address": set(["prefix"]),
    }


def csv_import(model, f, resolution=IR_FAIL):
    """
    Import from CSV
    :returns: (record_count,error_message).
              record_count is None if error_message set
    """
    ## Detect UTF8 BOM (EF BB BF)
    if not f.read(3) == "\xef\xbb\xbf":
        # No BOM found, seek to start
        f.seek(0)
    reader = csv.reader(f)
    # Process model fields
    field_names = set()
    required_fields = set()
    unique_fields = set([f.name for f in model._meta.fields if f.unique])
    fk = {}  # Foreign keys: name->(model,field)
    # find boolean fields
    booleans = set([f.name for f in model._meta.fields if
                    isinstance(f, models.BooleanField)])
    integers = set([f.name for f in model._meta.fields if
                    isinstance(f, models.IntegerField)])
    # Search for foreign keys and required fields
    ir = IGNORED_REQUIRED.get(model._meta.db_table, set())
    for name, required, rel, rname in get_model_fields(model):
        field_names.add(name)
        if rel:
            fk[name] = (rel, rname)
        if required and not name in ir:
            required_fields.add(name)
    # Read and validate header
    header = reader.next()
    left = field_names.copy()
    u_fields = [h for h in header if h in unique_fields]
    ut_fields = [fs for fs in model._meta.unique_together
                 if len(fs) == len([f for f in fs if f in header])]
    # Check field names
    for h in header:
        if h not in field_names:
            return None, "Invalid field '%s'" % h
        left.remove(h)
    # Check all required fields present
    for h in left:
        if h in required_fields:
            return None, "Required field '%s' is missed" % h
    # Load data
    count = 0
    l_header = len(header)
    for row in reader:
        count += 1
        if len(row) != l_header:
            return None, "Invalid row size. line %d" % count
        vars = dict(zip(header, row))
        for h, v in vars.items():
            # Check required field is not none
            if not v and h in required_fields:
                return None, "Required field '%s' is empty at line %d" % (
                h, count)
            # Delete empty values
            if not v:
                del vars[h]
            else:
                if h in fk:
                    # reference foreign keys
                    rel, rname = fk[h]
                    try:
                        ro = rel.objects.get(**{rname: v})
                    except rel.DoesNotExist:
                        # Failed to reference by name, fallback to id
                        try:
                            id = int(v)
                        except ValueError:
                            return None, "Cannot resolve '%s' in field '%s' at line '%s'" % (v, h, count)
                        try:
                            ro = rel.objects.get(**{"id": id})
                        except rel.DoesNotExist:
                            return None, "Cannot resolve '%s' in field '%s' at line '%s'" % (v, h, count)
                    vars[h] = ro
                elif h in booleans:
                    # Convert booleans
                    vars[h] = v.lower() in ["t", "true", "yes", "y"]
                elif h in integers:
                    # Convert integers
                    try:
                        vars[h] = int(v)
                    except ValueError, why:
                        raise ValueError("Invalid integer: %s" % why)
        # Find object
        o = None
        for f in u_fields:
            # Find by unique fields
            try:
                o = model.objects.get(**{f: vars[f]})
                break
            except model.DoesNotExist:
                pass
        if o is None and ut_fields:
            # Find by composite unique keys
            for fs in ut_fields:
                try:
                    o = model.objects.get(**dict([(f, vars[f]) for f in fs]))
                    break
                except model.DoesNotExist:
                    pass
        if o:
            # Object exists, behave according the resolution order
            if resolution == IR_FAIL:
                # Fail
                return None, "Failed to save line %d: Object %s is already exists" % (
                    count, repr(vars))
            elif resolution == IR_SKIP:
                # Skip line
                count -= 1
                continue
        else:
            # Create object
            o = model()
        # Set attributes
        for k, v in vars.items():
            setattr(o, k, v)
        # Save
        try:
            o.save()
        except Exception, why:
            return None, "Failed to save line %d: %s. %s" % (count, str(why),
                                                             repr(vars))
    return count, None
