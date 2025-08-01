import sys

class Output:
    def error(self, message: str):
        raise Exception(message)  # or a custom exception type

    def warning(self, message: str):
        print(f"Warning: {message}", file=sys.stderr)

    def fatal(self, message: str, *args):
        error_msg = f"Fatal error: {message}. "
        if args:
            error_msg += ' Params: '.join(str(arg) for arg in args)
        raise SystemExit(error_msg)
    
    def message(self, message: str):
        print(f"{message}")
